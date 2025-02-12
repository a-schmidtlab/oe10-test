
1. Recognizing the Command Pattern of the Mount
From the capture, I can see many lines that start with:
3C 03 3A 01 3A ...

followed by some bytes, and ending with
... 3A ?? 3A 47 3E

3C is the ASCII character <.
3E is the ASCII character >.
Inside, I will see repeated keywords in ASCII such as:
50 43 = "PC"
41 53 = "AS"
53 54 = "ST"
It looks like:
< 03 : 01 : 07 : PC :  ... : G>

Where the ... part in hex contains the parameters (speed, direction, etc.) for the motor movement.
“PC” Commands Appear to Control Motion
Looking at the log, the real “movement” commands all contain the PC (0x50 0x43) bytes. The bytes after PC : (i.e., after 50 43 3A) change depending on which direction/speed is being commanded. Then, almost immediately, a second command with PC : 00 00 00 00 ... is sent to stop the motion.
When I pressed the arrow keys, the log shows sequences like:
A non‐zero PC command (to start the motion in some direction).
A quick PC 00 00 00 00 (stop) command to end that motion.
For example (times truncated to keep it short):
[14:26:30] Written data:
   3C 03 3A 01 3A 07 3A 50 43 3A 08 00 1E 00 3A 00 3A 47 3E ...  (Start move)
[14:26:31] Written data:
   3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E    (Stop)

I can see that the first command has the bytes 08 00 1E 00 after 50 43 3A, whereas the stop command has 00 00 00 00.
By examining each distinct non‐zero PC command, I can map them to Up, Down, Left, Right. In the logs, I see four different parameter sets (plus the stop command):
08 00 1E 00
04 00 28 00
02 32 00 00
01 32 00 00
00 00 00 00 (Stop)
Each set shows up exactly when I pressed some arrow key. The differences in bytes (08 vs 04 vs 02 vs 01, and 1E vs 28 vs 32, etc.) likely encode direction and speed. In general:
The first 2 bytes (e.g., 08 00) might represent a direction code + small speed offset,
The next 2 bytes (e.g., 1E 00) might represent the speed (0x1E = 30 decimal, 0x28 = 40 decimal, 0x32 = 50 decimal),
or vice versa.
But the simplest way to replicate them is just to send exactly the same raw hex that appeared in Ir log.

2. Example “Movement” Commands in Hex
Below are the raw hex messages for each direction, taken directly from the capture. I can send these in CoolTerm in “Hex” mode (so it literally sends these bytes).
Important
Depending on Ir exact firmware or device, I might need to replicate the whole line (including the trailing bytes like 3A 16 3A 47 3E or 3A 25 3A 47 3E, etc.).
Also note in the logs, some commands appear twice in a row. Often software repeats them for reliability. Sending one copy is usually enough if the controller only needs a single command.
2.1 Up
From the log around 14:26:30, the command that starts the “Up” motion is:
3C 03 3A 01 3A 07 3A 50 43 3A 08 00 1E 00 3A 00 3A 47 3E

I can send that as Ir “Go Up” command.
Then, to stop (which was sent at 14:26:31):
3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E


2.2 Down
Shortly after I pressed the opposite arrow (the logs around 14:26:32), I see:
3C 03 3A 01 3A 07 3A 50 43 3A 04 00 28 00 3A 3A 3A 47 3E

Some log snippets show slightly different trailing bytes (like 3A 3A 3A 47 3E). This is presumably still the same fundamental “PC 04 00 28 00” command.
I would pair that with the stop command again:
3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E


2.3 Left
From around 14:26:34:
3C 03 3A 01 3A 07 3A 50 43 3A 02 32 00 00 3A 26 3A 47 3E

And then stop (the same stop as before).

2.4 Right
From around 14:26:35:
3C 03 3A 01 3A 07 3A 50 43 3A 01 32 00 00 3A 25 3A 47 3E

Then stop again.

3. Stop Command
I can see the stop command repeating in the log with slightly varying “:16:”, “:25:”, or “:26:” near the end. The simplest is just to replicate the exact line that appears most frequently:
3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E


4. Sending via CoolTerm
Hex Mode: In CoolTerm’s “Send String” dialog, I have to choose “Hex” rather than “ASCII”. Then paste the bytes (space‐separated or line‐separated). For instance:
3C 03 3A 01 3A 07 3A 50 43 3A 08 00 1E 00 3A 00 3A 47 3E


Send Then Delay: Often PTZ or motor controllers expect one move command, some time to act on it, then a stop. So I might:
Send the “Up” command,
Wait a second or so,
Send the “Stop” command.
Repeated Commands: In the logs, the software often duplicates the same command two or more times in a row. I typically only need to send it once, unless Ir specific device requires repeated triggers.

5. Summary of the Main “Move” Commands

Up
3C 03 3A 01 3A 07 3A 50 43 3A 08 00 1E 00 3A 00 3A 47 3E


Down
3C 03 3A 01 3A 07 3A 50 43 3A 04 00 28 00 3A 3A 3A 47 3E


Left
3C 03 3A 01 3A 07 3A 50 43 3A 02 32 00 00 3A 26 3A 47 3E


Right
3C 03 3A 01 3A 07 3A 50 43 3A 01 32 00 00 3A 25 3A 47 3E


Stop
3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E


(The exact trailing bytes like 3A 16 or 3A 25 may vary, but these should work as found in the log.)
That should let I directly replicate Up, Down, Left, Right, and Stop commands on Ir two‐axis mount via the same serial protocol I captured.

