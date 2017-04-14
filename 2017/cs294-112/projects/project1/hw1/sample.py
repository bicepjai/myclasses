import gym
env = gym.make('CartPole-v0')
for i_episode in range(1):
    observation = env.reset()
    for t in range(10):
        env.render()
        print(env.action_space)
        action = env.action_space.sample()
        print(observation,action)
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break