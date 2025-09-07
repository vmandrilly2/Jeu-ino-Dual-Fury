# Game Settings and Constants
import pygame

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Player settings
PLAYER_SIZE = 32
PLAYER_SPEED = 200  # pixels per second
PLAYER_ATTACK_COOLDOWN = 0.5  # seconds
PLAYER_ATTACK_DURATION = 0.2  # seconds
PLAYER_INVINCIBILITY_TIME = 1.0  # seconds after taking damage
PLAYER_HITBOX_SIZE = 48  # attack hitbox size

# Player 1 controls
PLAYER1_CONTROLS = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'attack': pygame.K_q
}

# Player 2 controls
PLAYER2_CONTROLS = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'attack': pygame.K_k
}

# Player starting stats
PLAYER_STARTING_HP = 100
PLAYER_STARTING_LEVEL = 1
PLAYER_STARTING_XP = 0
PLAYER_BASE_DAMAGE = 25

# XP and leveling
BASE_XP_REQUIREMENT = 25
XP_TIER_INCREASE = 25  # Additional XP per tier (every 5 levels)

# Enemy settings
ENEMY_SIZE = 24
ENEMY_BASE_SPEED = 50
ENEMY_BASE_HP = 50
ENEMY_BASE_DAMAGE = 10
ENEMY_HP_SCALING = 10  # HP increase per wave
ENEMY_XP_REWARD = 5

# Boss settings
BOSS_SIZE = 64
BOSS_BASE_HP = 500
BOSS_SPEED = 30
BOSS_DAMAGE = 25
BOSS_XP_REWARD = 50
BOSS_WAVE_INTERVAL = 5  # Boss appears every 5 waves

# Wave settings
WAVE_BASE_ENEMY_COUNT = 8
WAVE_ENEMY_INCREASE = 2  # Additional enemies per wave
WAVE_BREAK_TIME = 3.0  # seconds between waves

# UI settings
UI_FONT_SIZE = 24
UI_SMALL_FONT_SIZE = 18
UI_LARGE_FONT_SIZE = 36
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
XP_BAR_WIDTH = 150
XP_BAR_HEIGHT = 15
UI_MARGIN = 20

# Skill selection UI
SKILL_SELECTION_BACKGROUND_ALPHA = 180
SKILL_OPTION_WIDTH = 300
SKILL_OPTION_HEIGHT = 100
SKILL_OPTION_SPACING = 20

# Game states
GAME_STATE_MENU = 'menu'
GAME_STATE_PLAYING = 'playing'
GAME_STATE_SKILL_SELECTION = 'skill_selection'
GAME_STATE_GAME_OVER = 'game_over'
GAME_STATE_PAUSED = 'paused'

# Skill definitions
SKILLS = {
    # Attack skills
    'power_strike': {
        'name': 'Strong Strike',
        'description': 'Damage +10%',
        'type': 'attack',
        'max_level': 5,
        'effect': {'damage_multiplier': 0.1}
    },
    'sword_mastery': {
        'name': 'Sword Mastery',
        'description': 'Attack range +15%',
        'type': 'attack',
        'max_level': 3,
        'effect': {'range_multiplier': 0.15}
    },
    'critical_hit': {
        'name': 'Critical Hit',
        'description': '10% crit chance, 2x damage',
        'type': 'attack',
        'max_level': 1,
        'effect': {'crit_chance': 0.1, 'crit_multiplier': 2.0}
    },
    'whirlwind': {
        'name': 'Whirlwind',
        'description': 'Continuous spinning attack',
        'type': 'attack',
        'max_level': 1,
        'effect': {'whirlwind': True}
    },
    'shock_wave': {
        'name': 'Shock Wave',
        'description': 'Every 3rd attack sends projectile',
        'type': 'attack',
        'max_level': 1,
        'effect': {'shock_wave': True}
    },
    'execute': {
        'name': 'Execute',
        'description': 'Instantly kill low HP enemies',
        'type': 'attack',
        'max_level': 1,
        'effect': {'execute_threshold': 0.2}
    },
    
    # Defense skills
    'vitality': {
        'name': 'Vitality',
        'description': 'Max HP +20',
        'type': 'defense',
        'max_level': 5,
        'effect': {'max_hp_bonus': 20}
    },
    'life_steal': {
        'name': 'Life Steal',
        'description': '5% damage heals you',
        'type': 'defense',
        'max_level': 3,
        'effect': {'life_steal': 0.05}
    },
    'regeneration': {
        'name': 'Regeneration',
        'description': 'Heal 1% max HP every 5 seconds',
        'type': 'defense',
        'max_level': 3,
        'effect': {'regen_rate': 0.01, 'regen_interval': 5.0}
    },
    'dodge_dash': {
        'name': 'Dodge Dash',
        'description': 'Short invincible dash ability',
        'type': 'defense',
        'max_level': 1,
        'effect': {'dodge_dash': True}
    },
    'guardian_aura': {
        'name': 'Guardian Aura',
        'description': '10% damage reduction',
        'type': 'defense',
        'max_level': 3,
        'effect': {'damage_reduction': 0.1}
    },
    
    # Utility skills
    'frost_touch': {
        'name': 'Frost Touch',
        'description': 'Attacks slow enemies',
        'type': 'utility',
        'max_level': 1,
        'effect': {'slow_effect': 0.5, 'slow_duration': 2.0}
    },
    'stun_strike': {
        'name': 'Stun Strike',
        'description': '20% chance to stun enemies',
        'type': 'utility',
        'max_level': 1,
        'effect': {'stun_chance': 0.2, 'stun_duration': 1.5}
    },
    'swift_feet': {
        'name': 'Swift Feet',
        'description': 'Movement speed +10%',
        'type': 'utility',
        'max_level': 5,
        'effect': {'speed_multiplier': 0.1}
    },
    'magnet': {
        'name': 'Magnet',
        'description': 'Larger XP pickup range',
        'type': 'utility',
        'max_level': 3,
        'effect': {'pickup_range_multiplier': 0.5}
    },
    
    # Cooperation skills
    'leadership': {
        'name': 'Leadership',
        'description': 'Nearby ally +5% damage',
        'type': 'cooperation',
        'max_level': 3,
        'effect': {'ally_damage_bonus': 0.05, 'aura_range': 100}
    },
    'life_link': {
        'name': 'Life Link',
        'description': 'Share healing with ally',
        'type': 'cooperation',
        'max_level': 1,
        'effect': {'share_healing': True}
    },
    'teamwork': {
        'name': 'Teamwork',
        'description': 'Extra damage when attacking same target',
        'type': 'cooperation',
        'max_level': 1,
        'effect': {'teamwork_bonus': 0.25}
    },
    'battlefield_support': {
        'name': 'Battlefield Support',
        'description': 'Gain buffs when ally is low HP',
        'type': 'cooperation',
        'max_level': 1,
        'effect': {'support_threshold': 0.3, 'support_bonus': 0.2}
    }
}

# Particle effects
PARTICLE_LIFETIME = 1.0
BLOOD_PARTICLE_COUNT = 5
XP_PARTICLE_SPEED = 100

# Audio settings (for future implementation)
MASTER_VOLUME = 0.7
SFX_VOLUME = 0.8
MUSIC_VOLUME = 0.6