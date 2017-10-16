from gym import envs

environment_ID = [spec.id for spec in envs.registry.all()]

for env_ID in sorted(environment_ID):

    print(env_ID)