from shutil import copyfile
import time


def main():
	copyfile("database/xp_database/pet_xp_db.json", f'database/xp_database/pet_xp_db_backup.json')


main()
