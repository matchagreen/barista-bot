# Barista Bot

Personal discord bot developed in Python. Mostly just a youtube player for now. The commands are listed below:

### Play

Plays audio to the voice channel the requester is in.

Depending on the arguments and the state of the player, it resumes, starts playing a song, or adds a song to the end or start of the current playlist.

    /play [youtube-link] [order-to-add-to-playlist]


To play a song:

    /play https://www.youtube.com/watch?v=Y5VJnxDLaZY

To add next to playlist:

    /play https://www.youtube.com/watch?v=Y5VJnxDLaZY next

To add last to playlist:

    /play https://www.youtube.com/watch?v=Y5VJnxDLaZY last

To resume playing (when paused):

    /play

### Pause

Pauses audio.

    /pause

### Skip

Skips the current song.

    /skip

### Stop

Stops audio and clears the current paylist:

    /stop


![alt text](images/iced-matcha-latte.jpg)
