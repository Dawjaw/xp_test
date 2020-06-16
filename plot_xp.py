import pandas as pd
import plotly.graph_objects as go
from montydb import MontyClient
import time
from git import Repo
import git
from pathlib import Path
import os

PATH_OF_GIT_REPO = Path("F:\\Dawjaw.github.io\\.git")
COMMIT_MESSAGE = 'updated chart data'

pd.set_option('display.float_format', lambda x: '%.3f' % x)


def git_push():
	try:
		repo = Repo(PATH_OF_GIT_REPO)
		repo.git.add(update=True)
		repo.index.commit(COMMIT_MESSAGE)
		origin = repo.remote(name='origin')
		origin.push()
		print("Done")
	except git.GitCommandError as e:
		print(e)


def plot_minute_xp(collection):
	cursor = collection.find({})
	df = pd.DataFrame(list(cursor))

	if len(df) > 0:

		collectiondf = df
		collectiondf['readableTimestamp'] = pd.to_datetime(df['timestamp'], unit='ns')
		collectiondf['readableTimestamp'] = collectiondf['readableTimestamp'].dt.tz_localize('CET', ambiguous='infer')

		collection_no_df = collectiondf

		collection_no_df = collection_no_df.set_index('readableTimestamp')

		collectiondf['xp'] = collectiondf['xp'].diff()
		collectiondf = collectiondf.iloc[1:]
		collectiondf = collectiondf.set_index('readableTimestamp')

		collectiondf2 = collectiondf.resample("60Min").sum()

		collectiondf3 = collectiondf.resample("5Min").sum()

		# collectiondf = collectiondf[(collectiondf != 0).all(1)]

		fig2 = go.Figure()
		fig2.add_trace(go.Scatter(x=collectiondf2.index, y=collectiondf2['xp'], mode='lines',
								 name='hourly farming xp'))

		fig = go.Figure()
		fig.add_trace(go.Scatter(x=collectiondf3.index, y=collectiondf3['xp'], mode='lines',
								 name='minutly farming xp'))

		fig3 = go.Figure()
		fig3.add_trace(go.Scatter(x=collection_no_df.index, y=collection_no_df['xp'], mode='lines',
								 name='live farming xp'))


		with open('F:/Dawjaw.github.io/index.html', 'w') as f:
			f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
			f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
			f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))


def main():
	no_id = True

	client = MontyClient("database")
	db = client['xp_database']
	collection = db['pet_xp_db']
	

	plot_minute_xp(collection)
	git_push()


while True:
	try:
		main()
		time.sleep(60)
	except ConnectionResetError:
		continue

