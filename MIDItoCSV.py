import midi
import sys

if len(sys.argv) != 2:
    print("Usage: {0} <midifile>".format(sys.argv[0]))
    exit(0x02)

midi_filename = sys.argv[1]
if '.mid' in midi_filename:
    csv_filename = midi_filename.replace('.mid', '.csv')
else:
    exit(0x03)

pattern = midi.read_midifile(midi_filename)

csv_file = open(csv_filename, "w")

for track in pattern:

    current_channel = []
    current_channel.append(len(track))

    for event in track:

        # Note On event
        if 0b10010000 <= event.statusmsg <= 0b10011111:
            if event.name != "Note On":
                exit(0x10);
            if event.length != 2:
                exit(0x11)

            tick = event.tick
            pitch = event.data[0]
            velocity = event.data[1]

            current_channel.append(tick)
            current_channel.append(pitch)
            current_channel.append(velocity)

            if tick == 0:
                current_channel.append(0)
                current_channel.append(0)
            elif tick > 0b11111111:
                current_channel.append(0)
                current_channel.append((tick >> 8) & 0xFF)
                current_channel.append(tick & 0xFF)
            else:
                current_channel.append(tick)

            if pitch > 0b01111111:
                pitch = 0b01111111
            current_channel.append(pitch)

            if velocity > 0b01111111:
                velocity = 0b01111111
            current_channel.append(velocity)

    for i in range(len(current_channel)):
        csv_file.write(str(current_channel[i]))
        if i < len(current_channel)-1:
            csv_file.write(",")
    csv_file.write("\n")
