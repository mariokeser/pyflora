import repo_1 
import gui_1 


def main():
    db_client = repo_1.DbClient("./pyflora/Sensors/data/readings_1.db") 
    app = gui_1.App(db_client) 
    app.mainloop() 
    

if __name__ == "__main__": 
    main()