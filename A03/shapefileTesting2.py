import geopandas as gpd
import matplotlib.pyplot as plt
shapef=gpd.read_file("HIGHWAY_LINEAR_REF_SYSTEM_ARNOLD.shx")
# for line in shapef:
#     print(line)

print(shapef.shape)
print(shapef[0][0])

# shape.plot()
# plt.savefig("map.png")