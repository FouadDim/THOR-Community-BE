from bson import ObjectId
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
import uuid
from django.conf import settings
import os
import bcrypt
from .schemaValidators import *
import pymongo
from dotenv import load_dotenv
import json
from django.views.decorators.csrf import csrf_exempt


load_dotenv()

ACCOUNT_DB = settings.ACCOUNT_DB
PROJECT_DB = settings.PROJECT_DB

# Create your views here.
@api_view(["POST"])
def signup(request):
    
    user_id = str(uuid.uuid4())
    username = request.data.get("username")
    password = request.data.get("password")
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
                "username": username,
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
        
        
        
@api_view(["POST"])
def createOSP(request):
    
    user_id = request.data.get("user_id")
    username = request.data.get("username")
    project_id = str(uuid.uuid4())
    osp_title = request.data.get("osp_title")
    osp_description = request.data.get("osp_description")
    osp_topics = request.data.get("osp_topics")
    type = "osp"
    rating = 0
    members = 1
    
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


            old_opensource.append(project_id)

            # Use update_one on the collection, not on the account dictionary
            ACCOUNT_DB.accounts.update_one(
                {"user_id": user_id},
                {"$set": {"opensource": old_opensource}}
            )
            
            osp = {
                "user_id": user_id,
                "author": username,
                "project_id": project_id,
                "osp_title": osp_title,
                "osp_description": osp_description,
                "osp_topics": osp_topics,
                "type": type,
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
        print(e)
        return HttpResponse(e)
    
    
    
@api_view(["POST"])
def joinOSP(request):
    
    user_id = request.data.get("user_id")
    project_id = request.data.get("project_id")
    
    try:
        account = ACCOUNT_DB.accounts.find_one({"user_id": user_id})
        osp = PROJECT_DB.projects.find_one({"project_id": project_id})
        
        old_opensource = account.get("opensource", [])

        old_opensource.append(project_id)
        
        ACCOUNT_DB.accounts.update_one(
            {"user_id": user_id},
            {"$set": {"opensource": old_opensource}}
        )
        
        old_members = osp.get("members")
        new_members = old_members + 1
        
        PROJECT_DB.projects.update_one(
            {"project_id": project_id},
            {"$set": {"members": new_members}}
        )
        
        return JsonResponse({"status": 200, "message": "Joined Open Source Project!"})
    
    except Exception as e:
        print(e)
        return JsonResponse(
            {
                "status": 403,
                "message": "An Authentication Error Occurred. Try Again Later.",
            }
        )





@api_view(["POST"])
def getOSPs(request):
    
    user_id = request.data.get("user_id")
    
    try:
        account = ACCOUNT_DB.accounts.find_one({"user_id": user_id})

        opensource = account.get("opensource", [])

        matching_documents = []
        
        for opensource_id in opensource:
            
            osp = PROJECT_DB.projects.find_one({"project_id": opensource_id})
            
            if osp:
                matching_documents.append(osp)
        
        return JsonResponse({"status": 200, "payload": str(matching_documents)})
    
    except Exception as e:
        print(e)
        return JsonResponse(
            {
                "status": 403,
                "message": "An Authentication Error Occurred. Try Again Later.",
            }
        )
        
        

@api_view(["POST"])
def getOSP(request):
    
    user_id = request.data.get("user_id")
    
    try:
        osps_cursor = PROJECT_DB.projects.find({"user_id": user_id})
        
        # Convert the MongoDB cursor to a list of dictionaries
        osps_list = list(osps_cursor)
        
        # Convert ObjectId to string in each document
        for osp in osps_list:
            osp['_id'] = str(osp['_id'])
        
        # Now, you can include osps_list in your JSON response
        return JsonResponse({"status": 200, "payload": osps_list})
    
    except Exception as e:
        print(e)
        return JsonResponse(
            {
                "status": 403,
                "message": "An Authentication Error Occurred. Try Again Later.",
            }
        )


@api_view(["POST"])
def getOSPa(request):
    
    project_id = request.data.get("project_id")
    
    try:
        osps_cursor = PROJECT_DB.projects.find({"p_id": p_id})
        
        # Convert the MongoDB cursor to a list of dictionaries
        osps_list = list(osps_cursor)
        
        # Convert ObjectId to string in each document
        for osp in osps_list:
            osp['_id'] = str(osp['_id'])
        
        # Now, you can include osps_list in your JSON response
        return JsonResponse({"status": 200, "payload": osps_list})
    
    except Exception as e:
        print(e)
        return JsonResponse(
            {
                "status": 403,
                "message": "An Authentication Error Occurred. Try Again Later.",
            }
        )



@csrf_exempt
@api_view(["GET"])
def getAllOSP(request):
        
    try:
        osps_cursor = PROJECT_DB.projects.find({"type": "osp"})
        
        # Convert the MongoDB cursor to a list of dictionaries
        osps_list = list(osps_cursor)
        
        # Convert ObjectId to string in each document
        for osp in osps_list:
            osp['_id'] = str(osp['_id'])
        
        # Now, you can include osps_list in your JSON response
        return JsonResponse({"status": 200, "payload": osps_list})
    
    except Exception as e:
        print(e)
        return JsonResponse(
            {
                "status": 403,
                "message": "An Authentication Error Occurred. Try Again Later.",
            }
        )



@api_view(["POST"])
def checkVerified(request):
    
    user_id = request.data.get("user_id")
    
    try:
        account = ACCOUNT_DB.accounts.find_one({"user_id": user_id})
        
        if account.get("verified") == True:
            return HttpResponse("true")
        
        else:
            return HttpResponse("false")
        
    except:
        return HttpResponse(500)