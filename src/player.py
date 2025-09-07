import pygame
import math
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, player_id, x, y):
        super().__init__()
        self.player_id = player_id
        
        # Create player sprite
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE if player_id == 1 else RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Player stats
        self.max_hp = PLAYER_STARTING_HP
        self.hp = self.max_hp
        self.level = PLAYER_STARTING_LEVEL
        self.xp = PLAYER_STARTING_XP
        self.xp_to_next_level = self.calculate_xp_requirement()
        self.base_speed = PLAYER_SPEED
        self.base_damage = PLAYER_BASE_DAMAGE
        self.is_alive = True
        
        # Skills
        self.skills = {}
        
        # Combat
        self.attack_cooldown = 0
        self.attack_duration = 0
        self.is_attacking = False
        self.hitbox = None
        
        # Invincibility frames
        self.invincible_time = 0
        self.flash_timer = 0
        self.visible = True
        
        # Movement
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Controls based on player ID
        if player_id == 1:
            self.controls = PLAYER1_CONTROLS
        else:
            self.controls = PLAYER2_CONTROLS
            
        # Regeneration timer
        self.regen_timer = 0
        
        # Skill effects
        self.whirlwind_active = False
        self.shock_wave_counter = 0
        self.dodge_dash_cooldown = 0
        
    def calculate_xp_requirement(self):
        """Calculate XP required for next level based on tier system"""
        tier = (self.level - 1) // 5
        return BASE_XP_REQUIREMENT + (tier * XP_TIER_INCREASE)
    
    def get_effective_stats(self):
        """Calculate current stats with skill bonuses"""
        stats = {
            'speed': self.base_speed,
            'damage': self.base_damage,
            'max_hp': self.max_hp,
            'attack_range': PLAYER_HITBOX_SIZE,
            'crit_chance': 0,
            'crit_multiplier': 1.0,
            'damage_reduction': 0,
            'life_steal': 0
        }
        
        # Apply skill effects
        for skill_name, skill_level in self.skills.items():
            if skill_name in SKILLS:
                skill_data = SKILLS[skill_name]
                effect = skill_data['effect']
                
                if 'speed_multiplier' in effect:
                    stats['speed'] *= (1 + effect['speed_multiplier'] * skill_level)
                if 'damage_multiplier' in effect:
                    stats['damage'] *= (1 + effect['damage_multiplier'] * skill_level)
                if 'max_hp_bonus' in effect:
                    stats['max_hp'] += effect['max_hp_bonus'] * skill_level
                if 'range_multiplier' in effect:
                    stats['attack_range'] *= (1 + effect['range_multiplier'] * skill_level)
                if 'crit_chance' in effect:
                    stats['crit_chance'] += effect['crit_chance']
                if 'crit_multiplier' in effect:
                    stats['crit_multiplier'] = effect['crit_multiplier']
                if 'damage_reduction' in effect:
                    stats['damage_reduction'] += effect['damage_reduction'] * skill_level
                if 'life_steal' in effect:
                    stats['life_steal'] += effect['life_steal'] * skill_level
                    
        return stats
    
    def update(self, dt, keys_pressed, other_player=None):
        """Update player state"""
        if not self.is_alive:
            return
            
        # Update timers
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.attack_duration = max(0, self.attack_duration - dt)
        self.invincible_time = max(0, self.invincible_time - dt)
        self.dodge_dash_cooldown = max(0, self.dodge_dash_cooldown - dt)
        self.regen_timer += dt
        
        # Handle invincibility flashing
        if self.invincible_time > 0:
            self.flash_timer += dt
            if self.flash_timer >= 0.1:
                self.visible = not self.visible
                self.flash_timer = 0
        else:
            self.visible = True
            
        # Handle regeneration
        if 'regeneration' in self.skills and self.regen_timer >= 5.0:
            regen_amount = self.max_hp * 0.01 * self.skills['regeneration']
            self.heal(regen_amount)
            self.regen_timer = 0
            
        # Handle movement
        self.handle_movement(dt, keys_pressed)
        
        # Handle attack
        if self.attack_duration > 0:
            self.is_attacking = True
        else:
            self.is_attacking = False
            if self.hitbox:
                self.hitbox = None
                
        # Handle attack input
        if keys_pressed[self.controls['attack']] and self.attack_cooldown <= 0:
            self.attack()
            
    def handle_movement(self, dt, keys_pressed):
        """Handle player movement"""
        stats = self.get_effective_stats()
        speed = stats['speed']
        
        # Get movement input
        dx = 0
        dy = 0
        
        if keys_pressed[self.controls['left']]:
            dx -= 1
        if keys_pressed[self.controls['right']]:
            dx += 1
        if keys_pressed[self.controls['up']]:
            dy -= 1
        if keys_pressed[self.controls['down']]:
            dy += 1
            
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707
            
        # Apply movement
        self.velocity.x = dx * speed
        self.velocity.y = dy * speed
        
        # Update position
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
        
        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
    def attack(self):
        """Perform attack"""
        if self.attack_cooldown > 0:
            return
            
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.attack_duration = PLAYER_ATTACK_DURATION
        
        # Create hitbox
        stats = self.get_effective_stats()
        hitbox_size = int(stats['attack_range'])
        
        self.hitbox = pygame.Rect(
            self.rect.centerx - hitbox_size // 2,
            self.rect.centery - hitbox_size // 2,
            hitbox_size,
            hitbox_size
        )
        
        # Handle shock wave skill
        if 'shock_wave' in self.skills:
            self.shock_wave_counter += 1
            if self.shock_wave_counter >= 3:
                self.shock_wave_counter = 0
                # Create shock wave projectile (to be implemented)
                
    def take_damage(self, damage, other_player=None):
        """Take damage with invincibility frames"""
        if not self.is_alive or self.invincible_time > 0:
            return False
            
        stats = self.get_effective_stats()
        actual_damage = damage * (1 - stats['damage_reduction'])
        
        self.hp -= actual_damage
        self.invincible_time = PLAYER_INVINCIBILITY_TIME
        
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            
        return True
        
    def heal(self, amount):
        """Heal the player"""
        if not self.is_alive:
            return
            
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        actual_heal = self.hp - old_hp
        
        # Share healing with ally if life link skill is active
        return actual_heal
        
    def add_xp(self, amount):
        """Add experience points and handle leveling"""
        if not self.is_alive:
            return False
            
        self.xp += amount
        
        if self.xp >= self.xp_to_next_level:
            return self.level_up()
            
        return False
        
    def level_up(self):
        """Level up the player"""
        # Calculate overflow XP
        overflow_xp = self.xp - self.xp_to_next_level
        
        # Increase level
        self.level += 1
        
        # Calculate new XP requirement
        self.xp_to_next_level = self.calculate_xp_requirement()
        self.xp = overflow_xp
        
        # Full heal on level up
        old_max_hp = self.max_hp
        stats = self.get_effective_stats()
        self.max_hp = stats['max_hp']
        self.hp = self.max_hp
        
        return True  # Signal that skill selection should be triggered
        
    def add_skill(self, skill_name):
        """Add or upgrade a skill"""
        if skill_name in SKILLS:
            if skill_name in self.skills:
                if self.skills[skill_name] < SKILLS[skill_name]['max_level']:
                    self.skills[skill_name] += 1
            else:
                self.skills[skill_name] = 1
                
            # Apply immediate effects
            if skill_name == 'vitality':
                stats = self.get_effective_stats()
                old_max_hp = self.max_hp
                self.max_hp = stats['max_hp']
                self.hp += (self.max_hp - old_max_hp)  # Increase current HP too
                
    def get_available_skills(self):
        """Get list of skills that can be upgraded"""
        available = []
        for skill_name, skill_data in SKILLS.items():
            current_level = self.skills.get(skill_name, 0)
            if current_level < skill_data['max_level']:
                available.append(skill_name)
        return available
        
    def draw(self, screen):
        """Draw the player"""
        if self.visible:
            screen.blit(self.image, self.rect)
            
        # Draw attack hitbox for debugging
        if self.is_attacking and self.hitbox:
            pygame.draw.rect(screen, YELLOW, self.hitbox, 2)
            
    def get_center(self):
        """Get player center position"""
        return self.rect.center
        
    def distance_to(self, other_player):
        """Calculate distance to another player"""
        if not other_player:
            return float('inf')
        dx = self.rect.centerx - other_player.rect.centerx
        dy = self.rect.centery - other_player.rect.centery
        return math.sqrt(dx * dx + dy * dy)