# Game Settings and Constants
import pygame

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Language settings
CURRENT_LANGUAGE = 'zh'  # 'en' for English, 'zh' for Chinese - Default to Chinese

def toggle_language():
    """Toggle between English and Chinese"""
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE = 'zh' if CURRENT_LANGUAGE == 'en' else 'en'
    return CURRENT_LANGUAGE

# Translations
TRANSLATIONS = {
    'en': {
        'player': 'Player',
        'level': 'Level',
        'skills': 'Skills',
        'wave': 'Wave',
        'enemies': 'Enemies',
        'game_over': 'Game Over',
        'final_wave': 'Final Wave',
        'final_score': 'Final Score',
        'wave_break': 'Wave Break',
        'next_wave': 'Next Wave',
        'time_remaining': 'Time Remaining',
        'choose_skill': 'Choose a Skill',
        'press_number': 'Press number to select',
        'main_menu': 'Jeu-ino',
        'start_game': 'Start Game',
        'quit': 'Quit',
        'press_space': 'Press SPACE to start',
        'press_q': 'Press Q to quit'
    },
    'zh': {
        'player': '玩家',
        'level': '等级',
        'skills': '技能',
        'wave': '波次',
        'enemies': '敌人',
        'game_over': '游戏结束',
        'final_wave': '最终波次',
        'final_score': '最终得分',
        'wave_break': '波次间隔',
        'next_wave': '下一波',
        'time_remaining': '剩余时间',
        'choose_skill': '选择技能',
        'press_number': '按数字键选择',
        'main_menu': 'Jeu-ino',
        'start_game': '开始游戏',
        'quit': '退出',
        'press_space': '按空格键开始',
        'press_q': '按Q键退出'
    }
}

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
ENEMY_HP_SCALING = 5  # HP increase per wave (reduced from 10)
ENEMY_DAMAGE_SCALING = 2  # Damage increase per wave
ENEMY_XP_REWARD = 5

# Projectile settings
PROJECTILE_SPEED = 150
PROJECTILE_SIZE = 12  # Increased from 6 for better collision detection
ENEMY_SHOOT_COOLDOWN = 2.0
BOSS_SHOOT_COOLDOWN = 1.5
BOSS_SPECIAL_ATTACK_COOLDOWN = 5.0

# Boss settings
BOSS_SIZE = 64
BOSS_BASE_HP = 800  # Increased from 500
BOSS_SPEED = 60     # Increased from 30
BOSS_DAMAGE = 35    # Increased from 25
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
        'name_zh': '强力打击',
        'description': 'Damage +10%',
        'description_zh': '伤害 +10%',
        'type': 'attack',
        'max_level': 5,
        'effect': {'damage_multiplier': 0.1}
    },
    'sword_mastery': {
        'name': 'Sword Mastery',
        'name_zh': '剑术精通',
        'description': 'Attack range +15%',
        'description_zh': '攻击范围 +15%',
        'type': 'attack',
        'max_level': 3,
        'effect': {'range_multiplier': 0.15}
    },
    'critical_hit': {
        'name': 'Critical Hit',
        'name_zh': '致命一击',
        'description': '10% crit chance, 2x damage',
        'description_zh': '10% 暴击几率，2倍伤害',
        'type': 'attack',
        'max_level': 1,
        'effect': {'crit_chance': 0.1, 'crit_multiplier': 2.0}
    },
    'whirlwind': {
        'name': 'Whirlwind',
        'name_zh': '旋风斩',
        'description': 'Continuous spinning attack',
        'description_zh': '持续旋转攻击',
        'type': 'attack',
        'max_level': 1,
        'effect': {'whirlwind': True}
    },
    'shock_wave': {
        'name': 'Shock Wave',
        'name_zh': '冲击波',
        'description': 'Every 3rd attack sends projectile',
        'description_zh': '每第3次攻击发射投射物',
        'type': 'attack',
        'max_level': 1,
        'effect': {'shock_wave': True}
    },
    'execute': {
        'name': 'Execute',
        'name_zh': '处决',
        'description': 'Instantly kill low HP enemies',
        'description_zh': '瞬间击杀低血量敌人',
        'type': 'attack',
        'max_level': 1,
        'effect': {'execute_threshold': 0.2}
    },
    
    # Defense skills
    'vitality': {
        'name': 'Vitality',
        'name_zh': '生命力',
        'description': 'Max HP +20',
        'description_zh': '最大生命值 +20',
        'type': 'defense',
        'max_level': 5,
        'effect': {'max_hp_bonus': 20}
    },
    'life_steal': {
        'name': 'Life Steal',
        'name_zh': '生命偷取',
        'description': '5% damage heals you',
        'description_zh': '5% 伤害转化为治疗',
        'type': 'defense',
        'max_level': 3,
        'effect': {'life_steal': 0.05}
    },
    'regeneration': {
        'name': 'Regeneration',
        'name_zh': '生命恢复',
        'description': 'Heal 1% max HP every 5 seconds',
        'description_zh': '每5秒恢复1%最大生命值',
        'type': 'defense',
        'max_level': 3,
        'effect': {'regen_rate': 0.01, 'regen_interval': 5.0}
    },
    'dodge_dash': {
        'name': 'Dodge Dash',
        'name_zh': '闪避冲刺',
        'description': 'Short invincible dash ability',
        'description_zh': '短距离无敌冲刺技能',
        'type': 'defense',
        'max_level': 1,
        'effect': {'dodge_dash': True}
    },
    'guardian_aura': {
        'name': 'Guardian Aura',
        'name_zh': '守护光环',
        'description': '10% damage reduction',
        'description_zh': '减少10%受到的伤害',
        'type': 'defense',
        'max_level': 3,
        'effect': {'damage_reduction': 0.1}
    },
    
    # Utility skills
    'frost_touch': {
        'name': 'Frost Touch',
        'name_zh': '冰霜之触',
        'description': 'Attacks slow enemies',
        'description_zh': '攻击减缓敌人速度',
        'type': 'utility',
        'max_level': 1,
        'effect': {'slow_effect': 0.5, 'slow_duration': 2.0}
    },
    'stun_strike': {
        'name': 'Stun Strike',
        'name_zh': '眩晕打击',
        'description': '20% chance to stun enemies',
        'description_zh': '20% 几率眩晕敌人',
        'type': 'utility',
        'max_level': 1,
        'effect': {'stun_chance': 0.2, 'stun_duration': 1.5}
    },
    'swift_feet': {
        'name': 'Swift Feet',
        'name_zh': '迅捷步伐',
        'description': 'Movement speed +10%',
        'description_zh': '移动速度 +10%',
        'type': 'utility',
        'max_level': 5,
        'effect': {'speed_multiplier': 0.1}
    },
    'magnet': {
        'name': 'Magnet',
        'name_zh': '磁力',
        'description': 'Larger XP pickup range',
        'description_zh': '扩大经验值拾取范围',
        'type': 'utility',
        'max_level': 3,
        'effect': {'pickup_range_multiplier': 0.5}
    },
    
    # Cooperation skills
    'leadership': {
        'name': 'Leadership',
        'name_zh': '领导力',
        'description': 'Nearby ally +5% damage',
        'description_zh': '附近队友伤害 +5%',
        'type': 'cooperation',
        'max_level': 3,
        'effect': {'ally_damage_bonus': 0.05, 'aura_range': 100}
    },
    'life_link': {
        'name': 'Life Link',
        'name_zh': '生命链接',
        'description': 'Share healing with ally',
        'description_zh': '与队友共享治疗效果',
        'type': 'cooperation',
        'max_level': 1,
        'effect': {'share_healing': True}
    },
    'teamwork': {
        'name': 'Teamwork',
        'name_zh': '团队合作',
        'description': 'Extra damage when attacking same target',
        'description_zh': '攻击同一目标时额外伤害',
        'type': 'cooperation',
        'max_level': 1,
        'effect': {'teamwork_bonus': 0.25}
    },
    'battlefield_support': {
        'name': 'Battlefield Support',
        'name_zh': '战场支援',
        'description': 'Gain buffs when ally is low HP',
        'description_zh': '队友低血量时获得增益',
        'type': 'cooperation',
        'max_level': 1,
        'effect': {'support_threshold': 0.3, 'support_bonus': 0.2}
    },
    
    # Shooting skills
    'ranged_combat': {
        'name': 'Ranged Combat',
        'name_zh': '远程战斗',
        'description': 'Unlock shooting ability',
        'description_zh': '解锁射击能力',
        'type': 'shooting',
        'max_level': 1,
        'effect': {'ranged_combat': True}
    },
    'rapid_fire': {
        'name': 'Rapid Fire',
        'name_zh': '连射',
        'description': 'Shooting speed +50%',
        'description_zh': '射击速度 +50%',
        'type': 'shooting',
        'max_level': 3,
        'effect': {'fire_rate_multiplier': 0.5}
    },
    'piercing_shot': {
        'name': 'Piercing Shot',
        'name_zh': '穿透射击',
        'description': 'Projectiles pierce through enemies',
        'description_zh': '投射物穿透敌人',
        'type': 'shooting',
        'max_level': 1,
        'effect': {'piercing': True}
    },
    'explosive_shot': {
        'name': 'Explosive Shot',
        'name_zh': '爆炸射击',
        'description': 'Projectiles explode on impact',
        'description_zh': '投射物撞击时爆炸',
        'type': 'shooting',
        'max_level': 1,
        'effect': {'explosive': True, 'explosion_radius': 40}
    },
    'multi_shot': {
        'name': 'Multi Shot',
        'name_zh': '多重射击',
        'description': 'Fire 3 projectiles at once',
        'description_zh': '同时发射3个投射物',
        'type': 'shooting',
        'max_level': 1,
        'effect': {'multi_shot': 3}
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

# Language settings
CURRENT_LANGUAGE = 'zh'  # 'en' for English, 'zh' for Chinese - Default to Chinese

# Text translations
TRANSLATIONS = {
    'en': {
        'game_title': 'Dual Fury',
        'press_space_to_start': 'Press SPACE to start',
        'player_1_controls': 'Player 1: WASD to move, Q to attack',
        'player_2_controls': 'Player 2: Arrow keys to move, K to attack',
        'wave': 'Wave',
        'enemies_left': 'Enemies Left',
        'level': 'Level',
        'hp': 'HP',
        'xp': 'XP',
        'game_over': 'GAME OVER',
        'press_r_to_restart': 'Press R to restart',
        'choose_skill': 'Choose a skill:',
        'boss': 'BOSS',
        'wave_complete': 'Wave Complete!',
        'next_wave_in': 'Next wave in:'
    },
    'zh': {
        'game_title': '双人狂怒',
        'press_space_to_start': '按空格键开始游戏',
        'player_1_controls': '玩家1：WASD移动，Q攻击',
        'player_2_controls': '玩家2：方向键移动，K攻击',
        'wave': '波次',
        'enemies_left': '剩余敌人',
        'level': '等级',
        'hp': '生命值',
        'xp': '经验值',
        'game_over': '游戏结束',
        'press_r_to_restart': '按R键重新开始',
        'choose_skill': '选择技能：',
        'boss': '首领',
        'wave_complete': '波次完成！',
        'next_wave_in': '下一波倒计时：'
    }
}