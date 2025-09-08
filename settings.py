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
    },
    
    # Elemental skills
    'flame_weapon': {
        'name': 'Flame Weapon',
        'name_zh': '烈焰武器',
        'description': 'Attacks burn enemies for 3 seconds',
        'description_zh': '攻击使敌人燃烧3秒',
        'type': 'elemental',
        'max_level': 3,
        'effect': {'burn_damage': 5, 'burn_duration': 3.0}
    },
    'lightning_strike': {
        'name': 'Lightning Strike',
        'name_zh': '雷电打击',
        'description': 'Chain lightning to nearby enemies',
        'description_zh': '闪电链击附近敌人',
        'type': 'elemental',
        'max_level': 1,
        'effect': {'chain_lightning': True, 'chain_range': 80, 'chain_count': 3}
    },
    'poison_blade': {
        'name': 'Poison Blade',
        'name_zh': '毒刃',
        'description': 'Attacks poison enemies, reducing their speed',
        'description_zh': '攻击使敌人中毒，降低移动速度',
        'type': 'elemental',
        'max_level': 2,
        'effect': {'poison_damage': 3, 'poison_duration': 5.0, 'poison_slow': 0.3}
    },
    'ice_armor': {
        'name': 'Ice Armor',
        'name_zh': '冰甲',
        'description': 'Attackers are slowed for 2 seconds',
        'description_zh': '攻击者被减速2秒',
        'type': 'elemental',
        'max_level': 1,
        'effect': {'ice_armor': True, 'armor_slow': 0.4, 'armor_slow_duration': 2.0}
    },
    
    # Summoning skills
    'spirit_wolf': {
        'name': 'Spirit Wolf',
        'name_zh': '灵魂之狼',
        'description': 'Summon a wolf companion',
        'description_zh': '召唤狼灵伙伴',
        'type': 'summoning',
        'max_level': 1,
        'effect': {'summon_wolf': True, 'wolf_damage': 15, 'wolf_speed': 80}
    },
    'healing_orb': {
        'name': 'Healing Orb',
        'name_zh': '治疗法球',
        'description': 'Summon orb that heals nearby players',
        'description_zh': '召唤治疗附近玩家的法球',
        'type': 'summoning',
        'max_level': 2,
        'effect': {'healing_orb': True, 'orb_heal': 2, 'orb_range': 60}
    },
    'shadow_clone': {
        'name': 'Shadow Clone',
        'name_zh': '影分身',
        'description': 'Create a clone that mimics your attacks',
        'description_zh': '创造模仿你攻击的影分身',
        'type': 'summoning',
        'max_level': 1,
        'effect': {'shadow_clone': True, 'clone_damage': 0.5}
    },
    
    # Time skills
    'time_slow': {
        'name': 'Time Slow',
        'name_zh': '时间减缓',
        'description': 'Slow all enemies for 5 seconds (cooldown: 30s)',
        'description_zh': '减缓所有敌人5秒（冷却：30秒）',
        'type': 'time',
        'max_level': 1,
        'effect': {'time_slow': True, 'slow_factor': 0.3, 'slow_duration': 5.0, 'cooldown': 30.0}
    },
    'blink': {
        'name': 'Blink',
        'name_zh': '闪现',
        'description': 'Teleport short distance (cooldown: 8s)',
        'description_zh': '短距离传送（冷却：8秒）',
        'type': 'time',
        'max_level': 2,
        'effect': {'blink': True, 'blink_distance': 100, 'cooldown': 8.0}
    },
    'rewind': {
        'name': 'Rewind',
        'name_zh': '时光倒流',
        'description': 'Restore HP to 3 seconds ago (cooldown: 45s)',
        'description_zh': '恢复到3秒前的生命值（冷却：45秒）',
        'type': 'time',
        'max_level': 1,
        'effect': {'rewind': True, 'rewind_time': 3.0, 'cooldown': 45.0}
    },
    
    # Berserker skills
    'berserker_rage': {
        'name': 'Berserker Rage',
        'name_zh': '狂战士之怒',
        'description': 'Lower HP = Higher damage (max +50%)',
        'description_zh': '生命值越低伤害越高（最高+50%）',
        'type': 'berserker',
        'max_level': 1,
        'effect': {'berserker_rage': True, 'max_damage_bonus': 0.5}
    },
    'blood_frenzy': {
        'name': 'Blood Frenzy',
        'name_zh': '嗜血狂热',
        'description': 'Each kill increases attack speed for 10s',
        'description_zh': '每次击杀增加攻击速度10秒',
        'type': 'berserker',
        'max_level': 3,
        'effect': {'blood_frenzy': True, 'frenzy_bonus': 0.15, 'frenzy_duration': 10.0}
    },
    'last_stand': {
        'name': 'Last Stand',
        'name_zh': '背水一战',
        'description': 'Become invincible for 3s when HP drops below 20%',
        'description_zh': '生命值低于20%时无敌3秒',
        'type': 'berserker',
        'max_level': 1,
        'effect': {'last_stand': True, 'trigger_threshold': 0.2, 'invincible_duration': 3.0}
    },
    
    # Mystic skills
    'mana_shield': {
        'name': 'Mana Shield',
        'name_zh': '魔法护盾',
        'description': 'Absorb damage with mana instead of HP',
        'description_zh': '用魔法值而非生命值承受伤害',
        'type': 'mystic',
        'max_level': 1,
        'effect': {'mana_shield': True, 'mana_absorption': 0.5}
    },
    'arcane_missiles': {
        'name': 'Arcane Missiles',
        'name_zh': '奥术飞弹',
        'description': 'Auto-cast homing missiles every 3 seconds',
        'description_zh': '每3秒自动发射追踪飞弹',
        'type': 'mystic',
        'max_level': 2,
        'effect': {'arcane_missiles': True, 'missile_damage': 20, 'missile_interval': 3.0}
    },
    'spell_echo': {
        'name': 'Spell Echo',
        'name_zh': '法术回响',
        'description': '25% chance to repeat last attack',
        'description_zh': '25%几率重复上次攻击',
        'type': 'mystic',
        'max_level': 1,
        'effect': {'spell_echo': True, 'echo_chance': 0.25}
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

# Item system
ITEM_PICKUP_RANGE = 30
ITEM_LIFETIME = 30.0  # Items disappear after 30 seconds
ITEM_BOUNCE_HEIGHT = 10
ITEM_BOUNCE_SPEED = 2.0

# Item drop rates (probability)
ITEM_DROP_RATES = {
    'common': 0.3,    # 30% chance
    'uncommon': 0.15, # 15% chance
    'rare': 0.05,     # 5% chance
    'epic': 0.02,     # 2% chance
    'legendary': 0.005 # 0.5% chance
}

# Item definitions
ITEMS = {
    # Healing items
    'health_potion': {
        'name': 'Health Potion',
        'name_zh': '生命药水',
        'description': 'Restores 50 HP',
        'description_zh': '恢复50点生命值',
        'type': 'consumable',
        'rarity': 'common',
        'color': (255, 100, 100),  # Red
        'effect': {'heal': 50}
    },
    'mega_health_potion': {
        'name': 'Mega Health Potion',
        'name_zh': '超级生命药水',
        'description': 'Restores 150 HP',
        'description_zh': '恢复150点生命值',
        'type': 'consumable',
        'rarity': 'rare',
        'color': (255, 50, 50),  # Dark Red
        'effect': {'heal': 150}
    },
    
    # Mana items
    'mana_potion': {
        'name': 'Mana Potion',
        'name_zh': '魔法药水',
        'description': 'Restores 50 Mana',
        'description_zh': '恢复50点魔法值',
        'type': 'consumable',
        'rarity': 'common',
        'color': (100, 100, 255),  # Blue
        'effect': {'mana': 50}
    },
    
    # Temporary buff items
    'strength_elixir': {
        'name': 'Strength Elixir',
        'name_zh': '力量药剂',
        'description': '+50% damage for 30 seconds',
        'description_zh': '30秒内伤害+50%',
        'type': 'buff',
        'rarity': 'uncommon',
        'color': (255, 165, 0),  # Orange
        'effect': {'damage_boost': 0.5, 'duration': 30.0}
    },
    'speed_elixir': {
        'name': 'Speed Elixir',
        'name_zh': '速度药剂',
        'description': '+30% speed for 45 seconds',
        'description_zh': '45秒内速度+30%',
        'type': 'buff',
        'rarity': 'uncommon',
        'color': (0, 255, 255),  # Cyan
        'effect': {'speed_boost': 0.3, 'duration': 45.0}
    },
    'invincibility_potion': {
        'name': 'Invincibility Potion',
        'name_zh': '无敌药水',
        'description': 'Invincible for 5 seconds',
        'description_zh': '无敌5秒',
        'type': 'buff',
        'rarity': 'epic',
        'color': (255, 215, 0),  # Gold
        'effect': {'invincible': True, 'duration': 5.0}
    },
    
    # Permanent upgrade items
    'heart_crystal': {
        'name': 'Heart Crystal',
        'name_zh': '心之水晶',
        'description': 'Permanently increases max HP by 25',
        'description_zh': '永久增加25点最大生命值',
        'type': 'permanent',
        'rarity': 'rare',
        'color': (255, 20, 147),  # Deep Pink
        'effect': {'max_hp_increase': 25}
    },
    'power_crystal': {
        'name': 'Power Crystal',
        'name_zh': '力量水晶',
        'description': 'Permanently increases damage by 10%',
        'description_zh': '永久增加10%伤害',
        'type': 'permanent',
        'rarity': 'rare',
        'color': (255, 69, 0),  # Red Orange
        'effect': {'damage_increase': 0.1}
    },
    'agility_crystal': {
        'name': 'Agility Crystal',
        'name_zh': '敏捷水晶',
        'description': 'Permanently increases speed by 10%',
        'description_zh': '永久增加10%速度',
        'type': 'permanent',
        'rarity': 'rare',
        'color': (50, 205, 50),  # Lime Green
        'effect': {'speed_increase': 0.1}
    },
    
    # Special items
    'xp_orb': {
        'name': 'XP Orb',
        'name_zh': '经验法球',
        'description': 'Grants 100 XP',
        'description_zh': '获得100点经验值',
        'type': 'special',
        'rarity': 'uncommon',
        'color': (255, 255, 0),  # Yellow
        'effect': {'xp': 100}
    },
    'skill_scroll': {
        'name': 'Skill Scroll',
        'name_zh': '技能卷轴',
        'description': 'Instantly gain a random skill',
        'description_zh': '立即获得随机技能',
        'type': 'special',
        'rarity': 'epic',
        'color': (138, 43, 226),  # Blue Violet
        'effect': {'random_skill': True}
    },
    'phoenix_feather': {
        'name': 'Phoenix Feather',
        'name_zh': '凤凰羽毛',
        'description': 'Revive with full HP when killed',
        'description_zh': '死亡时满血复活',
        'type': 'special',
        'rarity': 'legendary',
        'color': (255, 140, 0),  # Dark Orange
        'effect': {'revive': True}
    },
    
    # Weapon enhancement items
    'sharpening_stone': {
        'name': 'Sharpening Stone',
        'name_zh': '磨刀石',
        'description': '+15% crit chance for 60 seconds',
        'description_zh': '60秒内暴击率+15%',
        'type': 'buff',
        'rarity': 'uncommon',
        'color': (169, 169, 169),  # Dark Gray
        'effect': {'crit_boost': 0.15, 'duration': 60.0}
    },
    'explosive_powder': {
        'name': 'Explosive Powder',
        'name_zh': '爆炸粉末',
        'description': 'Next 10 attacks explode',
        'description_zh': '接下来10次攻击带有爆炸效果',
        'type': 'buff',
        'rarity': 'rare',
        'color': (255, 99, 71),  # Tomato
        'effect': {'explosive_attacks': 10}
    }
}