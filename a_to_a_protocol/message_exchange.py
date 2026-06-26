# this file defines the classes for message exchange in the A-to-A protocol,
# including TextPart, DataPart, FilePart, and Message. 
# Each part class represents a different type of message content,
# while the Message class encapsulates the sender, receiver, and parts of the message.
class TextPart:
 
    def __init__(self,text):
        self.text=text
 
class DataPart:
 
    def __init__(self,data):
        self.data=data
 
class FilePart:
 
    def __init__(self,file):
        self.file=file
 
class Message:
 
    def __init__(self,sender,receiver):
 
        self.sender=sender
        self.receiver=receiver
        self.parts=[]
 
msg = Message(
    "Planner",
    "Executor"
)
 
msg.parts.append(
    TextPart("Deploy Application")
)
 
msg.parts.append(
    DataPart(
        {"env":"prod"}
    )
)
 
msg.parts.append(
    FilePart(
        "deployment.yaml"
    )
)
 
for part in msg.parts:
 
    if hasattr(part,"text"):
        print("TEXT:",part.text)
 
    if hasattr(part,"data"):
        print("DATA:",part.data)
 
    if hasattr(part,"file"):
        print("FILE:",part.file)