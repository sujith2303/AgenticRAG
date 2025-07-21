from vector_store import LocalFileLoader
import os


def create_db(vector_db, path : str):
    try:
        vector_db.load(path=path)
        return "Successfully loaded into db"
    except Exception as e:
        return e



if __name__=="__main__":
    file_loader = LocalFileLoader()
    base_path = "./database_pdfs"
    files = os.listdir(base_path)
    print(files)
    for file in files:
        create_db(file_loader,base_path + "/" + file)
    print("Successfully loaded files into DB")