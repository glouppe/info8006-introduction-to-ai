from gym.envs.registration import register

register(
    id='BerkeleyPacmanPO-v0',
    entry_point='gym_pacman.envs:PacmanEnv',
)
