#!/usr/bin/python3

from dataclasses import dataclass
import math
import sys

# print("Number of arguments: ", len(sys.argv), " arguments.")
# print("Argument List: ", str(sys.argv))

# Damage
# Value -> Damage
# Time -> Velocity


def clamp(x: int, min: int, max: int):
    x = min if x < min else x
    x = max if x > max else x
    return x


def velocityAtDistance(distance, muzzleVelocity, minVelocity, maxVelocity, minDeceleration, maxDeceleration):
    bulletDistance = 0
    timeStep = 1/60
    velocity = muzzleVelocity
    while (bulletDistance < distance):
        velocity = clamp(velocity, minVelocity, maxVelocity)
        lerp = (velocity - minVelocity) / (maxVelocity - minVelocity)
        deceleration = minDeceleration + lerp * (maxDeceleration - minDeceleration)
        tempVelocity = velocity - deceleration * timeStep
        tempDistance = bulletDistance + tempVelocity * timeStep

        # tempDistance

        if tempDistance > distance:
            return velocity

        velocity = tempVelocity
        bulletDistance = tempDistance

    return velocity


def nextBulletScan(distance, muzzleVelocity, minVelocity, maxVelocity, minDeceleration, maxDeceleration):
    bulletDistance = 0
    timeStep = 1/60
    velocity = muzzleVelocity
    while (True):
        velocity = clamp(velocity, minVelocity, maxVelocity)
        lerp = (velocity - minVelocity) / (maxVelocity - minVelocity)
        deceleration = minDeceleration + lerp * (maxDeceleration - minDeceleration)
        tempVelocity = velocity - deceleration * timeStep
        tempDistance = bulletDistance + tempVelocity * timeStep

        if tempDistance > distance:
            return tempDistance

        velocity = tempVelocity
        bulletDistance = tempDistance


def damageAtDistance(distance, muzzleVelocity, minVelocity, maxVelocity, minDeceleration, maxDeceleration, minDamage, maxDamage):
    velocity = velocityAtDistance(distance, muzzleVelocity, minVelocity, maxVelocity, minDeceleration, maxDeceleration)
    lerp = (velocity - minVelocity) / (maxVelocity - minVelocity)
    return minDamage + lerp * (maxDamage - minDamage)


def penetrationAtDistance(distance, muzzleVelocity, minVelocity, maxVelocity, minDeceleration, maxDeceleration, minPenetrationValue, maxPenetrationValue, minPenetrationTime, maxPenetrationTime, penetrationModifier):
    velocity = velocityAtDistance(distance, muzzleVelocity, minVelocity, maxVelocity, minDeceleration, maxDeceleration)
    lerp = (velocity - minPenetrationTime) / (maxPenetrationTime - minPenetrationTime)
    return minPenetrationValue + lerp * (maxPenetrationValue - minPenetrationValue) * penetrationModifier


def damageAtDistanceArmor(distance, muzzleVelocity, minVelocity, maxVelocity, minDeceleration, maxDeceleration, minArmorModifier, maxArmorModifier, minArmorPenetration, maxArmorPenetration, minPenetrationValue, maxPenetrationValue, minPenetrationTime, maxPenetrationTime, penetrationModifier, minDamage, maxDamage):
    velocity = velocityAtDistance(distance, muzzleVelocity, minVelocity, maxVelocity, minDeceleration, maxDeceleration)
    penetration = penetrationAtDistance(distance, muzzleVelocity, minVelocity, maxVelocity, minDeceleration, maxDeceleration,
                                        minPenetrationValue, maxPenetrationValue, minPenetrationTime, maxPenetrationTime, penetrationModifier)
    velocityMoltiplier = (maxArmorModifier - minArmorModifier) / (maxArmorPenetration - minArmorPenetration) * (penetration - minArmorPenetration) + minArmorModifier
    velocityAfterArmor = velocity * velocityMoltiplier

    lerp = (velocityAfterArmor - minVelocity) / (maxVelocity - minVelocity)
    return minDamage + lerp * (maxDamage - minDamage)


def shotsToKill(damage):
    return math.ceil(100/damage)


if len(sys.argv) == 1:
    sys.exit()


@ dataclass
class Fal:
    muzzleVelocity = 810*100
    minDamage = 10
    maxDamage = 130
    minVelocity = 5000
    maxVelocity = 100000
    minDeceleration = 0
    maxDeceleration = 150000
    minPenetrationValue = 50
    maxPenetrationValue = 500
    minPenetrationTime = 5000
    maxPenetrationTime = 100000
    penetrationModifier = 1


@ dataclass
class LightArmor:
    minModifier = 0.8
    maxModifier = 1.0
    minPenetration = 100
    maxPenetration = 500


@ dataclass
class HeavyArmor:
    minModifier = 0.6
    maxModifier = 0.9
    minPenetration = 100
    maxPenetration = 500


distance = float(sys.argv[1])*100
velocity = velocityAtDistance(distance, Fal.muzzleVelocity, Fal.minVelocity, Fal.maxVelocity, Fal.minDeceleration, Fal.maxDeceleration)
damage = damageAtDistance(distance, Fal.muzzleVelocity, Fal.minVelocity, Fal.maxVelocity, Fal.minDeceleration, Fal.maxDeceleration, Fal.minDamage, Fal.maxDamage)
penetration = penetrationAtDistance(distance, Fal.muzzleVelocity, Fal.minVelocity, Fal.maxVelocity, Fal.minDeceleration,
                                    Fal.maxDeceleration, Fal.minPenetrationValue, Fal.maxPenetrationValue, Fal.minPenetrationTime, Fal.maxPenetrationTime, Fal.penetrationModifier)
shots = shotsToKill(damage)
damageWithLightArmor = damageAtDistanceArmor(distance, Fal.muzzleVelocity, Fal.minVelocity, Fal.maxVelocity, Fal.minDeceleration, Fal.maxDeceleration, LightArmor.minModifier, LightArmor.maxModifier,
                                             LightArmor.minPenetration, LightArmor.maxPenetration, Fal.minPenetrationValue, Fal.maxPenetrationValue, Fal.minPenetrationTime, Fal.maxPenetrationTime, Fal.penetrationModifier, Fal.minDamage, Fal.maxDamage)
damageWithHeavyArmor = damageAtDistanceArmor(distance, Fal.muzzleVelocity, Fal.minVelocity, Fal.maxVelocity, Fal.minDeceleration, Fal.maxDeceleration, HeavyArmor.minModifier, HeavyArmor.maxModifier,
                                             HeavyArmor.minPenetration, HeavyArmor.maxPenetration, Fal.minPenetrationValue, Fal.maxPenetrationValue, Fal.minPenetrationTime, Fal.maxPenetrationTime, Fal.penetrationModifier, Fal.minDamage, Fal.maxDamage)
nextScan = nextBulletScan(distance, Fal.muzzleVelocity, Fal.minVelocity, Fal.maxVelocity, Fal.minDeceleration, Fal.maxDeceleration)

print("Meters:\t\t", distance/100)
print("Bullet Vel:\t", round(velocity/100, 2))
print("Damage:\t\t", round(damage, 2))
print("Penetration:\t", round(penetration, 2))
print("Shots to kill:\t", shots)
print("Damage LArmor:\t", round(damageWithLightArmor, 2))
print("Damage HArmor:\t", round(damageWithHeavyArmor, 2))
print("Next Scan:\t", round(nextScan/100, 2))
