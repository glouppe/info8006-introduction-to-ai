  This is a very simple particle filter example prompted by
Stanford's Intro to AI lectures.

  A robot is placed in a maze. It has no idea where it is, and
its only sensor can measure the approximate distance to the nearest
beacon (yes, I know it's totally weird, but it's easy to implement).
Also, it shows that even very simple sensors can be used, no need
for a high resolution laser scanner.

  In the arena display the robot is represented by a small green
turtle and its beliefs are red/blue dots. The more a belief matches
the current sensor reading, the more the belief's colour changes to
red. Beacons are little cyan dots. For illustration purposes, we
also compute the mean of all reasonably confident particles, then
check whether that point is actually a center of a cluster. This
point is represented by a gray circle, which becomes green when the
algorithm thinks it actually determined the robot's position.

  The robot then starts to randomly move around the maze. As it
moves, its beliefs are updated using the particle filter algorithm.
After a couple of moves, the beliefs converge around the robot. It
finally knows where it is!

  Particle filters really are totally cool...


  Start the simulation with:

    python particle_filter.py

  Feel free to experiment with different mazes, particles counts, etc.



  Enjoy!

        mjl
