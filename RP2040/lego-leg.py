import time
import machine
import mqtt_CBR
import valueMath
from secrets import home as homewifi
from secrets import Tufts_eecs as eecs
from umqtt.simple import MQTTClient

# mqtt stuff
mqtt_broker = '10.0.0.5' 
topic_sub = 'angle'
topic_pub = 'angle'
client_id = 'LEGO'

# Setting up LEDs
red = machine.PWM(machine.Pin(26))
red.freq(60)
green = machine.PWM(machine.Pin(27))
green.freq(60)
yellow = machine.PWM(machine.Pin(28))
yellow.freq(60)
white = machine.PWM(machine.Pin(29))
white.freq(60)

red.duty_u16(0)
green.duty_u16(0)
yellow.duty_u16(0)
white.duty_u16(0)

# Connecting to wifi
mqtt_CBR.connect_wifi(homewifi)
red.duty_u16(1000)
green.duty_u16(1000)
yellow.duty_u16(1000)
white.duty_u16(1000)
time.sleep(2)
green.duty_u16(0)
yellow.duty_u16(0)
white.duty_u16(0)

# Setting up adafruit io info
clientID = "7904a901-78d7-49bb-a245-838307f0b292"
url = "io.adafruit.com"
username = "ZhangBN"
aioKey = "aio_BPop04H7u7h3nZivmqDrPDjz1Zo4"
feedID1 = 'lego-leg'
feedID2 = 'lego-leg-2'
legoLeg1 = bytes('{:s}/feeds/{:s}'.format(username,feedID1),'utf-8')
legoLeg2 = bytes('{:s}/feeds/{:s}'.format(username,feedID2),'utf-8')

# Setting up led on the board
led = machine.Pin(6, machine.Pin.OUT)

# Angle stuff
# change in angles
theta1 = [-142.616801582135+90,0.273182931220646,-1.35629626251458,-2.53972588977945,-3.20956917969204,-3.12801029007454,-2.31344418735625,-1.03443576962286,0.177915709788181,1.24464720533047,2.05274729272654,2.44569634962753,2.45778491533034,2.32247184042137,2.29278992342657,2.36616123374785,2.43208916168368,2.39792818330014,2.28680411601414,2.30522528044793,2.58092363152284,3.07822583681667,3.68063218770762,4.36527255532894,5.17323872100441,5.8440999244354,6.18435597961066,6.04849850415172,5.41802807222543,4.08201163905319
]
theta2 = [77.9484765988481,1.31984709916364,3.57592324746462,5.21427969964255,6.12783644839372,6.02244535856509,4.97721036178956,3.37199910500405,1.86860028910071,0.523517876260243,-0.542259545826326,-1.10523626593509,-1.16207608095922,-1.00022900502414,-0.983874190593681,-1.12705653080822,-1.26834376758708,-1.25068292599356,-1.09433022882327,-1.15217733672156,-1.68660180151778,-2.68248170448688,-3.94255894869156,-5.39996231170979,-7.08217605307489,-8.42822224493355,-9.053430185999,-8.73176537007901,-7.50481415831803,-5.06129682961392
]
# absolute angles
Theta1 = [-142.616801582135,-142.343618650914,-143.699914913429,-146.239640803208,-149.449209982901,-152.577220272975,-154.890664460331,-155.925100229954,-155.747184520166,-154.502537314836,-152.449790022109,-150.004093672481,-147.546308757151,-145.22383691673,-142.931046993303,-140.564885759555,-138.132796597872,-135.734868414572,-133.448064298557,-131.142839018109,-128.561915386587,-125.48368954977,-121.803057362062,-117.437784806733,-112.264546085729,-106.420446161294,-100.236090181683,-94.1875916775312,-88.7695636053058,-84.6875519662526
]
Theta2 = [77.9484765988481,79.2683236980117,82.8442469454764,88.0585266451189,94.1863630935126,100.208808452078,105.186018813867,108.558017918871,110.426618207972,110.950136084232,110.407876538406,109.302640272471,108.140564191512,107.140335186488,106.156460995894,105.029404465086,103.761060697499,102.510377771505,101.416047542682,100.26387020596,98.5772684044423,95.8947866999555,91.9522277512639,86.5522654395541,79.4700893864792,71.0418671415457,61.9884369555467,53.2566715854677,45.7518574271497,40.6905605975357
]
valueMath.negative(theta1)
valueMath.negative(theta2)
valueMath.add(Theta1,90)
valueMath.negative(Theta1)
valueMath.negative(Theta2)

# Initiate io
io = MQTTClient(client_id=clientID,
                server=url,
                user=username,
                password=aioKey,
                port=1883)

# Connecting to io
try:            
    io.connect()
    print('Connection to Adafruit IO Successful')
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

# Process message from subscription for broker
def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    blink()
    time.sleep(0.5)
    blink()

# Process message from subscription for io
def sub_callback(topic,msg):
    print(msg)
    if msg == b'1':
        red.duty_u16(0)
        green.duty_u16(1000)
    elif msg == b'0':
        red.duty_u16(1000)
        green.duty_u16(0)

# Detecting on/off switch
def on_off():
    io.set_callback(sub_callback)
    io.subscribe(legoLeg1)
    print("Swtich to 'on' to start...")
    try:
        while True:
            io.wait_msg()
            if green.duty_u16()>0:
                break
    except KeyboardInterrupt as e:# manual stop if get stuck
            io.disconnect()
            red.duty_u16(0)
            green.duty_u16(0)
            print('Disconnected with IO')
            print('Done')

# Sending angles to broker and io
keyStop = 0
def main():
    fred = mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
    green.duty_u16(0)
    time.sleep(1)
    green.duty_u16(1000)
#     print('Trying to subscribe to topic:')
#     fred.subscribe(topic_sub)
#     print('Subscribed to topic',topic_sub)
    
    for i in range(len(theta1)):
        # sending angles to broker
        if i == 0:
            print('Sending angle to broker')
            print('.............')
        fred.publish(topic_pub, '(%f,%f)'%(theta1[i],theta2[i]))
        yellow.duty_u16(850)
        time.sleep(0.5)
        yellow.duty_u16(0)
        if i == len(theta1)-1:
            print('Finished sending angle to broker')
            print('--------------------------\n--------------------------')
    
    try:
        for i in range(len(Theta1)):
            # sending angles to io
            if i == 0:
                print('Sending angle to Adafruit IO')
                print('.............')
            # this format below is necessary to communicate to io
            io.publish(legoLeg1,bytes(str(Theta1[i]),'utf-8'),qos=0)
            io.publish(legoLeg2,bytes(str(Theta2[i]),'utf-8'),qos=0)
            white.duty_u16(850)
            time.sleep(0.5)
            white.duty_u16(0)
            
            time.sleep(1.5)
            
            if i == len(theta1)-1:
                print('Finished sending angle to Adafruit IO')
                print('--------------------------\n--------------------------')
        
    except OSError as e:
            print(e)
            fred.connect()
    except KeyboardInterrupt as e:
            keyStop = 1
            red.duty_u16(0)
            white.duty_u16(0)
            green.duty_u16(0)
            yellow.duty_u16(0)
            fred.disconnect()
            print('Finish sending angle to Adafruit IO')
            print('--------------------------\n--------------------------')
            print('Disconnected with broker')
            io.disconnect()
            print('Disconnected with IO')
            print('Done')

    if keyStop != 1:
        red.duty_u16(0)
        white.duty_u16(0)
        green.duty_u16(0)
        yellow.duty_u16(0)
        fred.disconnect()
        print('Disconnected with broker')
        io.disconnect()
        print('Disconnected with IO')
        print('Done')

# Calling out functions
on_off()
print('Started!')
main()