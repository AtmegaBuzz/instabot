from GenerateFollowers import get_followers
from Action import run_action


if __name__=='__main__':
    
   
    fake_insta_account = {
        "username":"arandomscript",
        "password":""
    }
    
    real_insta_account = {
        "username":"",
        "password":""
    }
    
    competitior_list = ["nasablackberry"]
    
    start = 100
    limit = 100
    
    # user edit section end ---------------------------------------------------
    
    print(
    """
        Choices:
            1 =  Generate followers.txt
            2 =  run action 
    """
    )
    choice = int(input("Choice: "))
    if(choice==1):
        get_followers(fake_insta_account["username"],fake_insta_account["password"],competitior_list,start=start,limit=limit)
    elif(choice==2):
        run_action(real_insta_account["username"],real_insta_account["password"])
    else:
        print("Invalid Choice")
