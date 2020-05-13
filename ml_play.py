"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import time
from mlgame.communication import ml as comm

def ml_loop(side: str):
    """
    The main loop for the machine learning process
    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```
    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    last_blocker_pos = (-1,-1)
    p_blocker = 0
    p_frame = -1
    ball_served = False
    def cut_to(player, speedx, way):
        if player == '1P':
            if way == 'same' :
                print("same cut")
                if speedx > 0:
                    return 1
                else:
                    return 2
            elif way == 'reverse':
                print("reserve cut")
                if speedx > 0:
                    return 2
                else:
                    return 1
    def move_to(player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+20  > (pred-10) and scene_info["platform_1P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_1P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left
        else :
            if scene_info["platform_2P"][0]+20  > (pred-10) and scene_info["platform_2P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left

    def ml_loop_for_1P(blocker_dir): 
        p_blocker = 0
        if scene_info["ball_speed"][1] > 0 : # 球正在向下 # ball goes down
            x = ( scene_info["platform_1P"][1]-scene_info["ball"][1] ) // scene_info["ball_speed"][1] # 幾個frame以後會需要接  # x means how many frames before catch the ball
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x)  # 預測最終位置 # pred means predict ball landing site 
            bound = pred // 200 # Determine if it is beyond the boundary
            if (bound > 0): # pred > 200 # fix landing position
                if (bound%2 == 0) : 
                    pred = pred - bound*200                    
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) : # pred < 0
                if (bound%2 ==1) :
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            if abs(scene_info["ball"][1]+5-scene_info["platform_1P"][1]) < scene_info["ball_speed"][1]:#scene_info["ball_speed"][1] > abs(scene_info["platform_1P"][1]-scene_info["ball"][1]-5)
                print("close to 1p plat")
                print("frame: ",scene_info["frame"])
                f = ( 160 ) // abs(scene_info["ball_speed"][1])
                print(f)
                speed_range = scene_info["frame"]//100
                p_blocker = f
                if (scene_info["frame"]+f)//100>speed_range:
                    f_n = (160-((speed_range+1)*100-scene_info["frame"])*abs(scene_info["ball_speed"][1]))//(abs(scene_info["ball_speed"][1])+1)
                    f = (speed_range+1)*100-scene_info["frame"]+f_n
                    p_blocker = f
                    print("new f",f)
                blocker_pred = scene_info["blocker"][0]+(5*blocker_dir*f)
                blocker_bound = blocker_pred // 200 # Determine if it is beyond the boundary
                if (blocker_bound > 0): # pred > 200 # fix landing position
                    if (blocker_bound%2 == 0) : 
                        blocker_pred = blocker_pred - blocker_bound*200                    
                    else :
                        blocker_pred = 200 - (blocker_pred - 200*blocker_bound)
                elif (blocker_bound < 0) : # pred < 0
                    if (blocker_bound%2 ==1) :
                        blocker_pred = abs(blocker_pred - (blocker_bound+1) *200)
                    else :
                        blocker_pred = blocker_pred + (abs(blocker_bound)*200)
                print("blocker now: ",scene_info["blocker"][0])
                print("blocker pred: ",blocker_pred)
                print("ball now: ",scene_info["ball"])
                print("ball speed now: ",abs(scene_info["ball_speed"][1]))
                cut_r = False
                cut_s = False

                if scene_info["ball_speed"][0] > 0: 
                    ball_pred = scene_info["ball"][0]+abs(scene_info["ball"][1]+5-scene_info["platform_1P"][1])+((scene_info["ball_speed"][0]+3)*f)
                else:
                    ball_pred = scene_info["ball"][0]-abs(scene_info["ball"][1]+5-scene_info["platform_1P"][1])+((scene_info["ball_speed"][0]-3)*f)
                ball_bound = ball_pred // 200 # Determine if it is beyond the boundary
                if (ball_bound > 0): # pred > 200 # fix landing position
                    if (ball_bound%2 == 0) : 
                        ball_pred = ball_pred - ball_bound*200                    
                    else :
                        ball_pred = 200 - (ball_pred - 200*ball_bound)
                elif (ball_bound < 0) : # pred < 0
                    if (ball_bound%2 ==1) :
                        ball_pred = abs(ball_pred - (ball_bound+1) *200)
                    else :
                        ball_pred = ball_pred + (abs(ball_bound)*200)
                cut_svalue =  0
                if (ball_pred+5 < blocker_pred-15 or ball_pred > blocker_pred+45):
                    cut_s = True
                    if ball_pred+5 < blocker_pred-10 :
                        cut_svalue =  blocker_pred - ball_pred+5
                    else:
                        cut_svalue =  ball_pred - blocker_pred+30
                print("cut s ball pred: ",ball_pred)

                if scene_info["ball_speed"][0] > 0: 
                    ball_pred = scene_info["ball"][0]+abs(scene_info["ball"][1]+5-scene_info["platform_1P"][1])+(-scene_info["ball_speed"][0]*f)
                else:
                    ball_pred = scene_info["ball"][0]-abs(scene_info["ball"][1]+5-scene_info["platform_1P"][1])+(-scene_info["ball_speed"][0]*f)
                ball_bound = ball_pred // 200 # Determine if it is beyond the boundary
                if (ball_bound > 0): # pred > 200 # fix landing position
                    if (ball_bound%2 == 0) : 
                        ball_pred = ball_pred - ball_bound*200                    
                    else :
                        ball_pred = 200 - (ball_pred - 200*ball_bound)
                elif (ball_bound < 0) : # pred < 0
                    if (ball_bound%2 ==1) :
                        ball_pred = abs(ball_pred - (ball_bound+1) *200)
                    else :
                        ball_pred = ball_pred + (abs(ball_bound)*200)

                cut_rvalue = 0
                if (ball_pred+5 < blocker_pred-15 or ball_pred > blocker_pred+45):
                    cut_r = True
                    if ball_pred+5 < blocker_pred-10 :
                        cut_rvalue =  blocker_pred - ball_pred+5
                    else:
                        cut_rvalue =  ball_pred - blocker_pred+30
                print("cut r ball pred: ",ball_pred)
                if cut_r and cut_s:
                    if cut_rvalue >= cut_svalue:
                        return cut_to(player = '1P',speedx= scene_info["ball_speed"][0],way = 'reverse'), p_blocker
                    else:
                        return cut_to(player = '1P',speedx= scene_info["ball_speed"][0],way = 'same'), p_blocker
                elif cut_r:
                    return cut_to(player = '1P',speedx= scene_info["ball_speed"][0],way = 'reverse'), p_blocker
                elif cut_s:
                    return cut_to(player = '1P',speedx= scene_info["ball_speed"][0],way = 'same'), p_blocker
                else:
                    return move_to(player = '1P',pred = pred), p_blocker
            else:
                if pred > 180:
                    return move_to(player = '1P',pred = 185), 0
                elif  pred < 20:
                    return move_to(player = '1P',pred = 15), 0
                else:
                    return move_to(player = '1P',pred = pred), 0
        else : # 球正在向上 # ball goes up
            return move_to(player = '1P',pred = 100), 0



    def ml_loop_for_2P():  # as same as 1P
        if scene_info["ball_speed"][1] > 0 : 
            return move_to(player = '2P',pred = 100)
        else : 
            x = ( scene_info["platform_2P"][1]+30-scene_info["ball"][1] ) // scene_info["ball_speed"][1] 
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x) 
            bound = pred // 200 
            if (bound > 0):
                if (bound%2 == 0):
                    pred = pred - bound*200 
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) :
                if bound%2 ==1:
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            return move_to(player = '2P',pred = pred)

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()
    t1 = 0
    t2 = 0
    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()
        if (scene_info["ball"][0]+5 >= scene_info["blocker"][0] and scene_info["ball"][0] < scene_info["blocker"][0]+30) and \
            abs(scene_info["ball"][1]-(scene_info["blocker"][1]+20)) < abs(scene_info["ball_speed"][1]) and scene_info["ball_speed"][1]<0:
            print("crush frame",scene_info["frame"],": ball x: ",scene_info["ball"]," blocker: ",scene_info["blocker"])
            print("ball speed now: ",abs(scene_info["ball_speed"][1]))
            print("crush!!!")
        if scene_info["frame"] == 0:
            t1 = time.monotonic()
        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False
            last_blocker_pos = (-1,-1)
            p_blocker = 0
            p_frame = -1
            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            t2 = time.monotonic()
            print("game time: {:8.3f}seconds".format(t2-t1))
            print("final speed: "+str(abs(scene_info["ball_speed"][1])))
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
            blocker_direct = 0
            if  last_blocker_pos[0] - scene_info["blocker"][0] > 0:
                blocker_direct = 1
            else:
                blocker_direct = -1
            #print("blocker speed",abs(last_blocker_pos[0] - scene_info["blocker"][0]))
            print("current frame :",scene_info["frame"]," ball: ",scene_info["ball"]," blocker: ",scene_info["blocker"])
            last_blocker_pos = scene_info["blocker"]

            if p_frame != -1 and scene_info["frame"] == p_frame:
                print("close frame",scene_info["frame"],": ball x: ",scene_info["ball"]," blocker: ",scene_info["blocker"])
                p_frame = -1
            if side == "1P":
                command, p_blocker= ml_loop_for_1P(-blocker_direct)
                if p_blocker != 0:
                    p_frame = scene_info["frame"]+p_blocker
                    print("p frame: ",p_frame)
                    p_blocker = 0
            else:
                command = ml_loop_for_2P()

            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})