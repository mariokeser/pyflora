import repo_1 , gui_1



def main():
    db_client = repo_1.DbClient("./pyflora/GUI/data/Pyflora.db") 
    app = gui_1.App(db_client) 
    app.mainloop() 
    

if __name__ == "__main__": 
   main()
