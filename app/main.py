from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection successful')
        break
    except Exception as error:
        print('Connection to database failed!')
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title":"title of post 1", "content": "content of post 1", "id": 1}, {"title":"favourite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


#this is called a path operation (or route)
#async is an async keyword for asynchronous development
#Name them as descriptive as possible
#return something - whatever is returned is sent to the user
#this is automatically converted to json

@app.get("/")
async def root():
    return {"message": "I can write APIs!!!"}

#the decorator forces it to act as an apis - get request to API
#HTTP methods for the main methods

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    #makes you resistant to SQL injection %%
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    #staged changes must be then pushed to the database
    conn.commit()
    return {"data": new_post}
# title str, content str, category, Bool


# ensure conversion (enforcing type definition in the function)
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    return {"post_detail": post}

@app.get("/posts/latest")
def get_latest_post():
    my_posts [len(my_posts)-1]
    return {"detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):


    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"post with id: {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return{"data": post_dict} 