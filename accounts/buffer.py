@api_view(["POST"])
def signup(request):
    
    user_id = str(uuid.uuid4())
    username = request.data.get(username)
    password = request.data.get(password)
    opensource=[]
    communities=[]
    verified = False
    
    if not username or not password:
        return JsonResponse({"status": 401, "message": "Add the needed info."})
    
    try:
        if ACCOUNT_DB.accounts.find_one({"username": username}):
            return JsonResponse(
                {
                    "status": 401,
                    "message": "A user with this username is already registered.",
                }
            )

        try:
            salt = bcrypt.gensalt(rounds=12)
            password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
            del password

            account = {
                "user_id": user_id,
                "password": str(password_hash),
                "opensource": opensource,
                "communities": communities,
                "verified": verified,
            }

            ACCOUNT_DB.command(
                {"collMod": "accounts", "validator": AccountValidator}
            )

            ACCOUNT_DB.accounts.create_index(
                [("username", pymongo.ASCENDING)], unique=True
            )
            ACCOUNT_DB.accounts.create_index(
                [("user_id", pymongo.ASCENDING)], unique=True
            )

            ACCOUNT_DB.accounts.insert_one(account)

            return JsonResponse(
                {"status": 200, "message": "Account added!"}
            )

        except pymongo.errors.PyMongoError as e:
            print(e)
            return JsonResponse(
                {
                    "status": 500,
                    "message": "A server error occurred. Please try again later.",
                }
            )

    except Exception as e:
        return HttpResponse(e)
    
    
    
    
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////




@api_view(["POST"])
def login(request):
    
    username = request.data.get("username")
    password = request.data.get("password")
    
    if not username or not password:
        return JsonResponse(
            {"status": 401, "message": "Please provide a username/password."}
        )

    try:
        account = ACCOUNT_DB.accounts.find_one({"username": username})

        if account is None:
            return JsonResponse(
                {"status": 401, "message": "Incorrect username/password combination."}
            )

        string_hashed_password = account["password"]
        hashed_password = string_hashed_password[2:-1]

        if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            del password

            user_id = account.get("user_id")
            username = account.get("username")
            verified = account.get("verified")


            payload = {
                "user_id": user_id,
                "username": username,
                "verified": verified,
            }

            return JsonResponse({"status": 200, "message": "Login Successful", "payload": payload})

        else:
            return JsonResponse(
                {"status": 401, "message": "Incorrect username/password combination."}
            )

    except:
        return JsonResponse(
            {
                "status": 403,
                "message": "An Authentication Error Occurred. Try Again Later.",
            }
        )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#/////////////////////////////////////////////////////////////////














@api_view(["POST"])
def createOSP(request):
    
    user_id = request.data.get("user_id")
    project_id = str(uuid.uuid4())
    osp_title = request.data.get("osp_title")
    osp_description = request.data.get("osp_description")
    osp_topics = request.data.get("osp_topics")
    osp_details = request.data.get("osp_details")
    rating = 0
    members = 0
    
    try:
        
        account = ACCOUNT_DB.accounts.find_one({"user_id": user_id})
        
        if PROJECT_DB.projects.find_one({"osp_title": osp_title}):
            return JsonResponse(
                {
                    "status": 401,
                    "message": "An Open Source Project with this name is already registered.",
                }
            )

        try:
            
            old_opensource = account.get("opensource", [])

            new_opensource = old_opensource.append(project_id)

            account.update_one(
                {"user_id": user_id},
                {"$set": {"opensource": new_opensource}}
            )
            
            osp = {
                "user_id": user_id,
                "project_id": project_id,
                "osp_title": osp_title,
                "osp_description": osp_description,
                "osp_topics": osp_topics,
                "osp_details": osp_details,
                "rating": rating,
                "members": members,
            }
            
            PROJECT_DB.command(
                {"collMod": "projects", "validator": projectValidator}
            )


            PROJECT_DB.projects.create_index(
                [("osp_title", pymongo.ASCENDING)], unique=True
            )
            PROJECT_DB.projects.create_index(
                [("project_id", pymongo.ASCENDING)], unique=True
            )


            PROJECT_DB.projects.insert_one(osp)

            return JsonResponse(
                {"status": 200, "message": "Open Source Project Created!"}
            )

        except pymongo.errors.PyMongoError as e:
            print(e)
            return JsonResponse(
                {
                    "status": 500,
                    "message": "A server error occurred. Please try again later.",
                }
            )

    except Exception as e:
        return HttpResponse(e)
    
    
    
    
    
    
    
    
    
    
    
    
    
    #?///////////////////////////////////////////////////////////////////////////////////////
    
    
    
    
    
    
    
    
    
    
    
    
@api_view(["POST"])
def joinOSP(request):
    
    user_id = request.data.get("user_id")
    project_id = request.data.get("project_id")
    
    try:
        account = ACCOUNT_DB.accounts.find_one({"user_id": user_id})
        osp = PROJECT_DB.projects.find_one({"project_id": project_id})

        old_opensource = account.get("opensource", [])

        new_opensource = old_opensource.append(project_id)

        account.update_one(
            {"user_id": user_id},
            {"$set": {"opensource": new_opensource}}
        )
        
        old_members = osp.get("members")
        new_members = old_members + 1
        
        osp.update_one(
            {"project_id": project_id},
            {"$set": {"members": new_members}}
        )
        
        return JsonResponse({"status": 200, "message": "Joined Open Source Project!"})
    
    except:
        return JsonResponse(
            {
                "status": 403,
                "message": "An Authentication Error Occurred. Try Again Later.",
            }
        )