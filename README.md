# Py OLC 3DGame Engine

### Origin
Port of the Olc 3D Game engine by [Javidx9](https://www.youtube.com/channel/UC-yuWVUplUJZvieEligKBkA) to a Python version, to learn more about 3d rendering.
This version lacks the features of part 4 atm since I haven't gotten around to doing it.

##Info
It is able to render most obj files, with 5 included in the repo.

File | Contents
---- | --------
empty.obj | A Completely empty obj used for testing in the past
axis.obj | Containing a 3d model of a axis marking the 3 axis. It is the default.
teapot.obj | The famous Utah Teapot model, which was the first Object to ever be modeled in 3d.
mountains.obj | A Mountain Range
VideoShip.obj | A Spaceship

If you want to change the file rendered, the string in [line 220 of main.py](https://github.com/Popaulol/Py-OLC-3DGameEngine/blob/0cc133e571a4d0630389499ff5040b213e1468c5/main.py#L220) has to be set to the correct file name.

## Bugs

There is a bug where it has problems with clipping Triangles correctly, I have not been able to fix it so far. If you have an Idea, please dm me on Discord (Staubfinger#8070) or open a PR.
If you find another bug, please also report/fix it that way.

I know that the code is not that clean, but I am cleaning up a bit atm.

## Requirements
It only has one requirement which is pynput for the controls.

## Controls
The controls are a bit wonky atm, but I am currently thinking about how to do them best.
Current Controls:

Key | Control
----| ------
w | move forward (relativ to camera)
s | move back (relativ to camera)
a | turn camera left
d | turn camera right
up| move up the y axis
down| move down the y axis
left| move along the absolute x axis (negative)
right| move along the absolute x axis (positive)

## Contributing
If you want to/already have fixed a bug, implemented a feature or do some refactoring feel free to open a PR or Issue.

But Please install [black](https://github.com/psf/black) and run [format.sh](https://github.com/Popaulol/Py-OLC-3DGameEngine/blob/master/format.sh) before every commit, or atleast have the last commit of the PR be running it.