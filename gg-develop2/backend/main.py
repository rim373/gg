from typing import Union,Optional,List,Annotated,Any
from fastapi import FastAPI, status , Depends ,HTTPException,UploadFile,File,Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

from database import *
from models import *
from schemas import *

# Initialize app
app = FastAPI()
 
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,  # Allow cookies or authorization headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)



# Create the database
Base.metadata.create_all(engine)

db_dependency = Annotated[Session,Depends(get_db)]


@app.delete("/Event/{id}", status_code=status.HTTP_204_NO_CONTENT, tags = ['Event'])
def delete_event(id: int, db:db_dependency  ):

    # get the event item with the given id
    event = db.query(EVENTREQUEST).get(id)


    #delelte question with given id
    if event:
        db.delete(event)
        db.commit()
    
    else:
        raise HTTPException(status_code=404, detail=f"event item with id {id} not found")

    return None




@app.post("/User",response_model=User, status_code=status.HTTP_201_CREATED ,tags = ['USER'])
def CreateUser(user:User, db:db_dependency ):
        
    # Create an instance of the Event database model
    userdb = UserRequest(
        Name=user.Name,
        Mail=user.Mail,
        pwd=user.pwd,
        IsAdmin=user.IsAdmin,
    )

    # Add it to the session and commit it
    db.add(userdb)
    db.commit()
    db.refresh(userdb)
    
    return userdb

@app.post("/Login", tags=['USER'])
def Login(login_request: LoginRequest, db: db_dependency):
    # Récupérer l'utilisateur depuis la base de données
    user = db.query(UserRequest).filter(UserRequest.Mail == login_request.Mail).first()

    # Vérifier si l'utilisateur existe
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")

    # Vérifier si le mot de passe correspond
    if login_request.pwd != user.pwd:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Mot de passe incorrect")

    return {
        "result": True,
        "data": {
            "Name": user.Name,
            "Mail": user.Mail,
            "pwd": user.pwd,
            "IsAdmin": user.IsAdmin,
        },
    }


  
  


@app.post("/Event",response_model=EventRequest, status_code=status.HTTP_201_CREATED ,tags = ['EventRequest'])
def create_event_request(event:EventRequest, db:db_dependency ):

    # create an instance of the Event database model
    
     # Create an instance of the Event database model
        eventdb = EVENTREQUEST(
            Content=event.Content,
            Organiser=event.Organiser,
            Date=event.Date,
            Flyer=str(event.Flyer),
        )

        # Add it to the session and commit it
        db.add(eventdb)
        db.commit()
        db.refresh(eventdb)

        # Return a success response
        return {
            "result": True,
            "message": "Event created successfully.",
            "data": {
                "Content": eventdb.Content,
                "Organiser": eventdb.Organiser,
                "Date": eventdb.Date,
                "Flyer": eventdb.Flyer,
            },
        }
        

@app.put("/Update_State/{id}", tags = ['EventResponse'])
def update_event_request(id: int, Accepted: bool):

    # create a new database session
    session = SessionLocal()

    # get the event request with the given id
    event = session.query(EVENTREQUEST).get(id)
    eventtest = session.query(EVENTREQUEST).all()
    l=[]
    for i in eventtest:
        if i.Accepted==True:
            date=i.Date
            l.append(date)
    if event.Date in l :
        raise HTTPException(status_code=404, detail=f"we have event in this date")
    else:
        # update event request with the given task (if an item with the given id was found)
    # update evnet request with the given task (if an item with the given id was found)
        if event:
            event.Accepted = Accepted
            session.commit()

    # close the session
    session.close()

    # check if event request with given id exists. If not, raise exception and return 404 not found response
    if not event:
        raise HTTPException(status_code=404, detail=f"Event item with id {id} not found")

    return EventResponse

@app.get("/accepted_events",response_model = List[EventResponse], tags = ['EventResponse'])
def read_accepted_events(db:db_dependency):
    # get all events
    
    question_list = db.query(EVENTREQUEST).all()
    finallist=[]
    
    for question in question_list :
        
        
        if question.Accepted==True :
            event=EventResponse
            event.Content=question.Content
            event.Organiser=question.Organiser
            event.Date=question.Date
            event.Flyer=question.Flyer
            event.Accepted=question.Accepted
            finallist.append(event)


    return finallist
@app.get("/event_request",response_model = List[EventRequestwithID], tags = ['EventRequest'])
def read_accepted_events(db:db_dependency):
    # get all events
    
    question_list = db.query(EVENTREQUEST).all()
    

    return question_list



'''pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_pwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, cin: int):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

@app.post("/login/" ,tags = ['login'])
async def login(request : UserItem , db:db_dependency):
    user= db.query(UserTable).filter(UserTable.cin == request.cin)
    if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"invalid user" )
    if not verify_pwd(request.password,user.password) :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"invalid password" )
    return none


@app.post("/User",response_model=UserItem, status_code=status.HTTP_201_CREATED, tags = ['users'])
def create_user(u:UserItem, db:db_dependency ):
    hashedpwd =pwd_context.hash(u.password)
    # create an instance of the user database model
    userdb =UserTable(cin = u.cin , full_name = u.full_name , Email = u.Email , password =hashedpwd)

    # add it to the session and commit it
    db.add(userdb)
    db.commit()
    db.refresh(userdb)
    
    return userdb 





def render_picture(data: bytes) -> str:
    return base64.b64encode(data).decode('ascii')


'''

""" @app.post("/test",response_model=QuestionRequest, status_code=status.HTTP_201_CREATED , tags = ['QA'])
async def create_question_pic(q:QuestionRequest,db:db_dependency, pic :UploadFile = File(...)):
    

    thread = threading.Thread(target=create_question, args=(q,db,))

    # Start the thread
    thread.start()

    # Wait for the thread to finish
    thread.join()


   # qdb = db.query(Question).filter(Question.content == q.id).first()

    #thread1 = threading.Thread(target=upload, args=(db,qdb.id, pic ,))

    # Start the thread
    #thread1.start()

    # Wait for the thread to finish
   # thread1.join()
     
    return None  """



'''
@app.post("/q",response_model=QuestionRequest, status_code=status.HTTP_201_CREATED ,tags = ['QA'])
def create_question(q:QuestionRequest, db:db_dependency ):

    # create an instance of the question database model
    qdb =Question(content = q.content)

    # add it to the session and commit it
    db.add(qdb)
    db.commit()
    db.refresh(qdb)
    
    # create an instance of the responses database model
    for choice in q.choices :
        choice_db =Response(response_text=choice.response_text,is_correct=choice.is_correct,question_id=qdb.id)
        db.add(choice_db)
    db.commit()
    
    
    return qdb 

@app.get("/users", tags = ['users'])
def get_users(db:db_dependency):
   
    # get the user items 
    userlist = db.query(UserTable).all()
    return userlist 

@app.get("/",response_model = List[QuestionRequest], tags = ['QA'])
def read_all_questions(db:db_dependency):
    # get all questions
    question_list = db.query(Question).all()
    finallist=[]
    #k=0
    for question in question_list :
        response = db.query(Response).filter(Response.question_id == question.id).all()
        l=[]
        for i in response:
            res=ResponseItem
            res.response_text=i.response_text
            res.is_correct=i.is_correct
            l.append(res)
        qa=QuestionRequest
        qa.content=question.content
        qa.choices=l
        
        finallist.append(qa)


    return finallist





@app.get("/q/{id}/", tags = ['QA'])
def read_question(id: int,db:db_dependency):
   
    # get the quetions item with the given id
    question = db.query(Question).get(id)
    response = db.query(Response).filter(Response.question_id == id).all()
    

    if not question:
        raise HTTPException(status_code=404, detail=f"the question with id {id} not found")
    r=dict()
    k=0
    for i in response:
        k+=1
        res=dict()
        res["response"]=i.response_text
        res["is correct"]=i.is_correct
        r[k]=res
        


    return {"question":question.content,"responses":r}



    
   

@app.put("/q/{id}", tags = ['QA'])
def update_question(id: int, content: str):

    # create a new database session
    session = SessionLocal()

    # get the question item with the given id
    question = session.query(Question).get(id)

    # update question item with the given task (if an item with the given id was found)
    if question:
        question.content = content
        session.commit()

    # close the session
    session.close()

    # check if quetion item with given id exists. If not, raise exception and return 404 not found response
    if not question:
        raise HTTPException(status_code=404, detail=f"question item with id {id} not found")

    return question



@app.put("/r/{id_question}/{id_response}", tags = ['QA'])
def update_response(id_question: int,id_response:int , newresponseitem: str,db:db_dependency):


 

   # get the question item with the given id
    question= db.query(Question).get(id_question)

     # check if quetion item with given id exists. If not, raise exception and return 404 not found response
    if not question :
        raise HTTPException(status_code=404, detail=f"question item with id {id_question} not found")
    
    # get the question item with the given id
    response = db.query(Response).filter(Response.question_id==id_question).all()

    # update question item with the given task (if an item with the given id was found)
    test = "false"
    if response:
        for i in response:
            if i.id == id_response:
                test = "true"
                i.response_text = newresponseitem
                db.commit()
          

   


    if test=="false" :
        raise HTTPException(status_code=404, detail=f"response item with id {id_response} in the question {id_question} not found")


    return {"question":question.content,"response":newresponseitem}




@app.put("/upload", status_code=status.HTTP_201_CREATED, tags = ['QA'])
async def upload( db:db_dependency,image_question: int = 0, pic :UploadFile = File(...)):

    question = db.query(Question).filter(Question.id == image_question).first()
    if not question  :
        raise HTTPException(status_code=404, detail=f"the question with id {image_question} not found")
    else:
        
    
        # Read the file data
        data = await pic.read()
    
    
        # Render picture data
        render_file = render_picture(data)
    
        # Create a new file record
    
        filedb = ImageTable(data=data,rendered_data=render_file,name=pic.filename,image_question=image_question)
        
        db.add(filedb)
        try:
            db.commit()
            db.refresh(filedb)
        except DataError as e:
            db.rollback()  # Rollback the transaction in case of an error
            return f"Error inserting data: {e}"
        
    

    asyncio.sleep(10)
    return None


@app.delete("/q/{id}", status_code=status.HTTP_204_NO_CONTENT, tags = ['QA'])
def delete_question(id: int,db:db_dependency):

    # get the quetion item with the given id
    question = db.query(Question).get(id)

    # get the responses for the question with the given id
    response=db.query(Response).filter(Response.question_id==id)

    #delete responses related to this question
    if response :
        for i in response :
            db.delete(i)
            db.commit()

    #delelte question with given id
    if question:
        db.delete(question)
        db.commit()
    
    else:
        raise HTTPException(status_code=404, detail=f"question item with id {id} not found")

    return None


@app.delete("/res/{id_question}/{id_response}", status_code=status.HTTP_204_NO_CONTENT, tags = ['QA'])
def delete_response(id_question: int,id_response:int,db:db_dependency):

    
     # get  the question with the given id
     question= db.query(Question).get(id_question)

    # get the responses item for the question with the given id
     response= db.query(Response).filter(Response.question_id==id_question).all()

     test = "false"
     # if question item with given id exists, delete it from the database. Otherwise raise 404 error
     for i in response :
         if i.id == id_response :
             test = "true" 
             db.delete(i)
             db.commit()
             
     if not question  :
         raise HTTPException(status_code=404, detail=f"question item with id {id_question} not found")
     if test=="false" :
         raise HTTPException(status_code=404, detail=f"response item with id {id_response} in the question {id_question} not found")


     return f"response with id ={id_response} of the question {question.id} is delated"

'''



'''@app.post("/q/pic",response_model=QuestionRequest, status_code=status.HTTP_201_CREATED)
async def add_image( db:db_dependency,file: UploadFile = File(...),img: ImageItem):
    content = await file.read()
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{uuid.uuid4().hex}{ext}'
    
 
    async with aiofiles.open(file_name, "wb") as f:
        await f.write(content)
    query = product.insert().values(title=payload.name, description=payload.description, image=????????)
    return await database.execute(query=query)'''


""" 
@app.get("/res/{id}")
def read_responses(id: int):
     # create a new database session
    session = SessionLocal()

    # get the responses for the question with id
    question= session.query(Question).filter(Question.id == id).all()

    # close the session
    session.close()

    if not question:
        raise HTTPException(status_code=404, detail=f"the question with id {id} has not a response")
    finallist =dict()
    for i in question :
        finallist[i.id]=i.response

    return  finallist



@app.post("/r/{id}", status_code=status.HTTP_201_CREATED)
def create_response(id:int):
    session = SessionLocal()
    question = session.query(Question).get(id)
    if question is None:
        raise HTTPException(status_code=404, detail=f"the question with id {id} not found")

     # create an instance of the respponse database model
    rdb = Response(correction = r.correction) 
    rdb.question_id = id

     # add it to the session and commit it
    session.add(rdb)
    session.commit()
    session.refresh(rdb)

        # close the session
    session.close()
     

    # return the id
    return rdb




 """
# @app.delete("/res/{id_question}/{id_response}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_response(id_question: int,id_response:int):

#     # create a new database session
#     session = SessionLocal()

#     # get the responses item for the question with the given id
#     response= session.query(Question).filter(Question.question_id == id_question).all()
#     test = "false"
#     # if question item with given id exists, delete it from the database. Otherwise raise 404 error
#     for i in response :
#         if i.id == id_response :
#             test = "true" 
#             session.delete(i)
#             session.commit()
#             session.close()
#     if not response  :
#         raise HTTPException(status_code=404, detail=f"question item with id {id_question} not found")
#     if test=="false" :
#         raise HTTPException(status_code=404, detail=f"response item with id {id_response} in the question {id_question} not found")


#     return None



""" @app.get("/q/r")
def read_question_responses():
    session = SessionLocal()
    finallist = []

    # Fetch all questions
    questions = session.query(Question).all()

    # Loop through each question
    for question in questions:
        question_dict = {
            "question_content": question.content,
            "responses": []
        }

        # Fetch responses for the current question
        responses = session.query(Question).filter(Question.question_id == question.id).all()

        # Loop through responses and append to question_dict
        for response in responses:
            response_dict = {
                "response_id": response.id,
                "response_correction": response.correction
            }
            question_dict["responses"].append(response_dict)

        finallist.append(question_dict)

    # Close the session
    session.close()

    return finallist
 """