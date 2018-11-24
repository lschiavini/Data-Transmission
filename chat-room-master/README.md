# Multi-Threaded-Chat-Room
*** README CHAT SYSTEM ***

NAME : SAVITHRU M LOKANATH
SOURCE FILE : [savithru_server.py, savithru_client.py]
MULTI-THREADING ENABLED
TIME OUT ENABLED
LOG FILES & PASSWORD/USERNAME STOREFILE PATH : /Users/savithru/Desktop/user_pass.txt

Steps to implement a chat system on your local machine - 

1) Download the compressed file Savithru.Lokanath.prog1.tar.gz & EXTRACT the files
2) PLACE the extracted folder named SavithruLokanath-Assignment4 in your local disk & OPEN it
3) OPEN the command prompt/terminal & RUN the chat_server using this command - 
   python savithru_server.py
4) OPEN another tab in the the command prompt/terminal & RUN the chat_client using this command - 
   python savithru_client.py
   For multiple clients repeat STEP 4
5) Create username & follow instructions
6) When prompted enter the option you desire 
6) This chat system supports Private chat, Broadcast Chat & File Transfers. The file will be stores in the directory    
   where the chat client is running 
7) Returning users can directly login without having to go throught the initial process
8) A log file named chatserver.log & chatclient.log will be created in the working directory which stores all the 
   information required  
9) Multi-Threading can be tested by opening multiple chat sessions with multiple clients

IMPORTANT : The program won't create a file for storing the user passwords & usernames. 
            Please create a file user_pass.txt on your Desktop (/Users/savithru/Desktop/) 

ERRORS EXPERIENCING :

1) New port address has to be assigned on each re-run. Checked on the internet, it's an OS feature that disables re-use of ports
2) If using a mp3 file, please save the target as .mp3 & open using the media player
