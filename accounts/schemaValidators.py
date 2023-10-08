AccountValidator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "user_id",
            "username",
            "password",
            "opensource",
            "communities",
        ],
        "properties": {
            "user_id": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "password": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "opensource": {
                "bsonType": "array",
                "description": "must be a string and is required",
            },
            "communities": {
                "bsonType": "array",
                "description": "must be a string and is required",
            },
        },
    }
}



projectValidator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "user_id",
            "author",
            "project_id",
            "osp_title",
            "osp_description",
            "osp_topics",
            "type",
            "rating",
            "members",
        ],
        "properties": {
            "user_id": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "author": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "project_id": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "osp_title": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "osp_description": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "osp_topics": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "rating": {
                "bsonType": "int",
                "description": "must be an int and is required",
            },
            "members": {
                "bsonType": "int",
                "description": "must be an int and is required",
            },
        },
    }
}