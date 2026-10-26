import asyncio
from mavsdk import System

async def run():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected"); break

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("GPS OK"); break
    async for pos in drone.telemetry.position():
        print(pos.latitude_deg, pos.longitude_deg, pos.absolute_altitude_m, pos.relative_altitude_m); break
    latitude = pos.latitude_deg
    longitude = pos.longitude_deg
    absAltitude = pos.absolute_altitude_m
    relAltitude = pos.relative_altitude_m
    spotA = (latitude + 6, longitude + 6, absAltitude + 1, relAltitude)
    spotB = (latitude -4, longitude + 3, absAltitude + 3, relAltitude)
    spotC = (latitude - 2, longitude -10, absAltitude +5, relAltitude)
    
    #actions
    await drone.action.set_takeoff_altitude(5.0)
    await drone.action.arm()
    await drone.action.takeoff()
    await drone.action.goto_location(latitude + 5, longitude + 5, absAltitude + 5, relAltitude)
    await asyncio.sleep(10)
    print(f"Going to {spotB}")
    await drone.action.goto_location(*spotB)
    await asyncio.sleep(10)
    print(f"Going to {spotC}")
    await drone.action.goto_location(*spotC)
    await asyncio.sleep(10)
    print(f"Landing")
    await drone.action.land()

asyncio.run(run())
