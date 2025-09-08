import pygame
import math
import random
from settings import *

class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, speed=PROJECTILE_SPEED, damage=10, color=WHITE):
        super().__init__()
        self.image = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0
            
        self.damage = damage
        self.lifetime = 3.0  # seconds
        
    def update(self, dt):
        """Update projectile position"""
        self.rect.x += self.velocity_x * dt
        self.rect.y += self.velocity_y * dt
        
        self.lifetime -= dt
        
        # Remove if off screen or lifetime expired
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or 
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.lifetime <= 0):
            self.kill()
            
    def draw(self, screen):
        """Draw the projectile"""
        screen.blit(self.image, self.rect)
        
    def check_collision(self, target_rect):
        """Check collision with target"""
        return self.rect.colliderect(target_rect)

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
        self.max_mana = 100  # Add mana system for item effects
        self.mana = self.max_mana
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
        
        # New skill effects
        self.burn_effects = {}  # enemy_id: (damage, duration)
        self.poison_effects = {}  # enemy_id: (damage, duration, slow)
        self.time_slow_cooldown = 0
        self.blink_cooldown = 0
        self.rewind_cooldown = 0
        self.rewind_hp_history = []  # Store HP values for rewind
        self.blood_frenzy_stacks = 0
        self.blood_frenzy_timer = 0
        self.last_stand_triggered = False
        self.last_stand_timer = 0
        self.arcane_missiles_timer = 0
        self.spell_echo_last_attack = None
        
        # Item buff effects
        self.damage_boost_timer = 0
        self.damage_boost_multiplier = 1.0
        self.speed_boost_timer = 0
        self.speed_boost_multiplier = 1.0
        self.crit_boost_timer = 0
        self.crit_boost_amount = 0
        self.invincible_timer = 0
        self.explosive_attacks_remaining = 0
        self.has_phoenix_feather = False
        
        # Shooting system
        self.projectiles = pygame.sprite.Group()
        self.shoot_cooldown = 0
        self.can_shoot = True  # Basic shooting ability available from start
        
        # Key press tracking for long press detection
        self.attack_key_pressed = False
        self.attack_key_hold_time = 0
        self.long_press_threshold = 0.5  # 500ms for long press
        self.special_weapon_cooldown = 0
        
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
            'life_steal': 0,
            'shoot_speed': 1.0,
            'projectile_speed': 1.0,
            'projectile_damage': 1.0,
            'piercing': 0,
            'multi_shot': 1,
            'explosive_damage': 0
        }
        
        # Apply berserker rage damage bonus
        if 'berserker_rage' in self.skills:
            hp_ratio = self.hp / self.max_hp
            damage_bonus = (1 - hp_ratio) * SKILLS['berserker_rage']['effect']['max_damage_bonus']
            stats['damage'] *= (1 + damage_bonus)
        
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
                    
            # Handle shooting skills
            if skill_name == 'ranged_combat':
                self.can_shoot = True
            elif skill_name == 'rapid_fire':
                stats['shoot_speed'] *= (1 + 0.3 * skill_level)  # 30% faster per level
            elif skill_name == 'piercing_shot':
                stats['piercing'] += skill_level
            elif skill_name == 'explosive_shot':
                stats['explosive_damage'] += 20 * skill_level
            elif skill_name == 'multi_shot':
                stats['multi_shot'] += skill_level
        
        # Apply item buff effects
        if self.damage_boost_timer > 0:
            stats['damage'] *= self.damage_boost_multiplier
        if self.speed_boost_timer > 0:
            stats['speed'] *= self.speed_boost_multiplier
        if self.crit_boost_timer > 0:
            stats['crit_chance'] += self.crit_boost_amount
                    
        return stats
    
    def update(self, dt, keys_pressed, other_player=None, enemies=None):
        """Update player state"""
        if not self.is_alive:
            return
            
        # Store enemies reference for shooting
        self.enemies = enemies if enemies else []
            
        # Update timers
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.attack_duration = max(0, self.attack_duration - dt)
        self.invincible_time = max(0, self.invincible_time - dt)
        self.dodge_dash_cooldown = max(0, self.dodge_dash_cooldown - dt)
        self.shoot_cooldown = max(0, self.shoot_cooldown - dt)
        self.special_weapon_cooldown = max(0, self.special_weapon_cooldown - dt)
        self.regen_timer += dt
        
        # Update new skill timers
        self.time_slow_cooldown = max(0, self.time_slow_cooldown - dt)
        self.blink_cooldown = max(0, self.blink_cooldown - dt)
        self.rewind_cooldown = max(0, self.rewind_cooldown - dt)
        self.blood_frenzy_timer = max(0, self.blood_frenzy_timer - dt)
        self.last_stand_timer = max(0, self.last_stand_timer - dt)
        self.arcane_missiles_timer += dt
        
        # Update item buff timers
        self.damage_boost_timer = max(0, self.damage_boost_timer - dt)
        self.speed_boost_timer = max(0, self.speed_boost_timer - dt)
        self.crit_boost_timer = max(0, self.crit_boost_timer - dt)
        self.invincible_timer = max(0, self.invincible_timer - dt)
        
        # Reset multipliers when timers expire
        if self.damage_boost_timer <= 0:
            self.damage_boost_multiplier = 1.0
        if self.speed_boost_timer <= 0:
            self.speed_boost_multiplier = 1.0
        if self.crit_boost_timer <= 0:
            self.crit_boost_amount = 0
        
        # Update rewind HP history
        if 'rewind' in self.skills:
            self.rewind_hp_history.append((self.hp, dt))
            # Keep only last 3 seconds of history
            total_time = 0
            for i in range(len(self.rewind_hp_history) - 1, -1, -1):
                total_time += self.rewind_hp_history[i][1]
                if total_time > 3.0:
                    self.rewind_hp_history = self.rewind_hp_history[i:]
                    break
        
        # Handle blood frenzy decay
        if self.blood_frenzy_timer <= 0 and self.blood_frenzy_stacks > 0:
            self.blood_frenzy_stacks = max(0, self.blood_frenzy_stacks - 1)
            if self.blood_frenzy_stacks > 0:
                self.blood_frenzy_timer = 10.0  # Reset timer for remaining stacks
        
        # Handle last stand
        if 'last_stand' in self.skills and not self.last_stand_triggered:
            if self.hp / self.max_hp <= SKILLS['last_stand']['effect']['trigger_threshold']:
                self.last_stand_triggered = True
                self.last_stand_timer = SKILLS['last_stand']['effect']['invincible_duration']
                self.invincible_time = self.last_stand_timer
        
        # Reset last stand when HP is restored
        if self.last_stand_triggered and self.hp / self.max_hp > 0.5:
            self.last_stand_triggered = False
        
        # Update projectiles
        self.projectiles.update(dt)
        
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
                
        # Handle attack input with long press detection
        attack_key_current = keys_pressed[self.controls['attack']]
        
        if attack_key_current:
            if not self.attack_key_pressed:
                # Key just pressed
                self.attack_key_pressed = True
                self.attack_key_hold_time = 0
                # Perform immediate melee attack if cooldown allows
                if self.attack_cooldown <= 0:
                    self.attack()
            else:
                # Key is being held
                self.attack_key_hold_time += dt
                
                # Check for long press special weapon
                if (self.attack_key_hold_time >= self.long_press_threshold and 
                    self.can_shoot and self.special_weapon_cooldown <= 0):
                    self.use_special_weapon()
                    self.special_weapon_cooldown = 2.0  # 2 second cooldown for special weapons
                    self.attack_key_hold_time = 0  # Reset to prevent spam
        else:
            if self.attack_key_pressed:
                # Key just released
                if (self.attack_key_hold_time < self.long_press_threshold and 
                    self.can_shoot and self.shoot_cooldown <= 0):
                    # Short press - regular shooting
                    self.shoot_forward(self.enemies)
            self.attack_key_pressed = False
            self.attack_key_hold_time = 0
            
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
        
        # Track last movement direction for shooting
        if dx != 0 or dy != 0:
            self.last_direction = (dx, dy)
        
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
                
    def shoot_forward(self, enemies=None):
        """Shoot a projectile towards the nearest enemy or in facing direction"""
        if not self.can_shoot or self.shoot_cooldown > 0:
            return
            
        stats = self.get_effective_stats()
        
        # Try to target nearest enemy first
        target_enemy = None
        if enemies:
            min_distance = float('inf')
            for enemy in enemies:
                distance = math.sqrt((enemy.rect.centerx - self.rect.centerx)**2 + 
                                   (enemy.rect.centery - self.rect.centery)**2)
                if distance < min_distance:
                    min_distance = distance
                    target_enemy = enemy
        
        # Determine shooting direction
        if target_enemy:
            # Shoot towards nearest enemy
            dx = target_enemy.rect.centerx - self.rect.centerx
            dy = target_enemy.rect.centery - self.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 0:
                dx /= distance
                dy /= distance
        else:
            # Fallback to movement direction or default
            if hasattr(self, 'last_direction') and self.last_direction:
                dx, dy = self.last_direction
            else:
                # Default to shooting upward
                dx, dy = 0, -1
            
        # Create projectile(s)
        projectile_speed = PROJECTILE_SPEED * stats['shoot_speed']
        projectile_damage = stats['damage'] // 2  # Shooting does less damage than melee
        
        # Handle multi-shot
        if 'multi_shot' in stats and stats['multi_shot'] > 1:
            num_shots = stats['multi_shot']
            angle_spread = 0.3  # Radians
            
            for i in range(num_shots):
                # Calculate angle offset
                offset = (i - (num_shots - 1) / 2) * angle_spread / (num_shots - 1) if num_shots > 1 else 0
                
                # Rotate direction
                cos_offset = math.cos(offset)
                sin_offset = math.sin(offset)
                
                shot_dx = dx * cos_offset - dy * sin_offset
                shot_dy = dx * sin_offset + dy * cos_offset
                
                # Create projectile
                target_x = self.rect.centerx + shot_dx * 1000
                target_y = self.rect.centery + shot_dy * 1000
                
                projectile = PlayerProjectile(
                    self.rect.centerx, self.rect.centery,
                    target_x, target_y,
                    speed=projectile_speed,
                    damage=projectile_damage
                )
                
                self.projectiles.add(projectile)
        else:
            # Single shot
            target_x = self.rect.centerx + dx * 1000
            target_y = self.rect.centery + dy * 1000
            
            projectile = PlayerProjectile(
                self.rect.centerx, self.rect.centery,
                target_x, target_y,
                speed=projectile_speed,
                damage=projectile_damage
            )
            
            self.projectiles.add(projectile)
            
        # Set cooldown
        base_cooldown = 0.3  # Base shooting cooldown
        self.shoot_cooldown = base_cooldown / stats['shoot_speed']
        
    def use_special_weapon(self):
        """Use special weapon based on unlocked skills"""
        if not self.can_shoot:
            return
            
        stats = self.get_effective_stats()
        
        # Explosive shot - creates area damage
        if 'explosive_shot' in self.skills:
            self.create_explosive_shot()
        # Piercing shot - shoots through enemies
        elif 'piercing_shot' in self.skills:
            self.create_piercing_shot()
        # Multi-shot burst
        elif 'multi_shot' in self.skills:
            self.create_multi_shot_burst()
        else:
            # Default special: rapid fire burst
            self.create_rapid_fire_burst()
            
    def create_explosive_shot(self):
        """Create an explosive projectile"""
        if hasattr(self, 'last_direction') and self.last_direction:
            dx, dy = self.last_direction
        else:
            dx, dy = 0, -1
            
        target_x = self.rect.centerx + dx * 1000
        target_y = self.rect.centery + dy * 1000
        
        # Create a larger, slower projectile that explodes
        projectile = PlayerProjectile(
            self.rect.centerx, self.rect.centery,
            target_x, target_y,
            speed=PROJECTILE_SPEED * 0.7,
            damage=self.get_effective_stats()['damage'],
            color=(255, 165, 0)  # Orange color for explosive
        )
        
        self.projectiles.add(projectile)
        
    def create_piercing_shot(self):
        """Create a piercing projectile"""
        if hasattr(self, 'last_direction') and self.last_direction:
            dx, dy = self.last_direction
        else:
            dx, dy = 0, -1
            
        target_x = self.rect.centerx + dx * 1000
        target_y = self.rect.centery + dy * 1000
        
        # Create a fast piercing projectile
        projectile = PlayerProjectile(
            self.rect.centerx, self.rect.centery,
            target_x, target_y,
            speed=PROJECTILE_SPEED * 1.5,
            damage=self.get_effective_stats()['damage'] // 2,
            color=(0, 255, 255)  # Cyan color for piercing
        )
        
        self.projectiles.add(projectile)
        
    def create_multi_shot_burst(self):
        """Create a burst of projectiles in multiple directions"""
        num_shots = 8
        for i in range(num_shots):
            angle = (i / num_shots) * 2 * math.pi
            dx = math.cos(angle)
            dy = math.sin(angle)
            
            target_x = self.rect.centerx + dx * 1000
            target_y = self.rect.centery + dy * 1000
            
            projectile = PlayerProjectile(
                self.rect.centerx, self.rect.centery,
                target_x, target_y,
                speed=PROJECTILE_SPEED * 0.8,
                damage=self.get_effective_stats()['damage'] // 3,
                color=(255, 255, 0)  # Yellow color for multi-shot
            )
            
            self.projectiles.add(projectile)
            
    def create_rapid_fire_burst(self):
        """Create a rapid fire burst"""
        if hasattr(self, 'last_direction') and self.last_direction:
            dx, dy = self.last_direction
        else:
            dx, dy = 0, -1
            
        # Fire 3 quick shots
        for i in range(3):
            target_x = self.rect.centerx + dx * 1000
            target_y = self.rect.centery + dy * 1000
            
            projectile = PlayerProjectile(
                self.rect.centerx, self.rect.centery,
                target_x, target_y,
                speed=PROJECTILE_SPEED * 1.2,
                damage=self.get_effective_stats()['damage'] // 3
            )
            
            self.projectiles.add(projectile)
    
    def shoot(self, target_x, target_y):
        """Legacy method for compatibility - now redirects to shoot_forward"""
        self.shoot_forward(self.enemies if hasattr(self, 'enemies') else None)
                
    def take_damage(self, damage, attacker=None):
        """Take damage with invincibility frames"""
        if not self.is_alive or self.invincible_time > 0:
            return False
            
        # Check for invincibility potion effect
        if self.invincible_timer > 0:
            return False
            
        stats = self.get_effective_stats()
        actual_damage = damage * (1 - stats['damage_reduction'])
        
        # Handle mana shield
        if 'mana_shield' in self.skills and self.mana > 0:
            mana_absorption = SKILLS['mana_shield']['effect']['mana_absorption']
            mana_damage = actual_damage * mana_absorption
            hp_damage = actual_damage * (1 - mana_absorption)
            
            mana_used = min(self.mana, mana_damage * 2)  # 2 mana per 1 damage absorbed
            self.mana -= mana_used
            absorbed_damage = mana_used / 2
            
            actual_damage = hp_damage + max(0, mana_damage - absorbed_damage)
        
        self.hp -= actual_damage
        self.invincible_time = PLAYER_INVINCIBILITY_TIME
        
        # Check for death and phoenix feather
        if self.hp <= 0 and self.has_phoenix_feather:
            self.hp = self.max_hp  # Revive with full HP
            self.has_phoenix_feather = False  # Consume the feather
            self.invincible_time = 3.0  # 3 seconds of invincibility after revival
            return False  # Didn't actually die
        
        # Handle ice armor effect
        if 'ice_armor' in self.skills and attacker and hasattr(attacker, 'apply_slow'):
            effect = SKILLS['ice_armor']['effect']
            attacker.apply_slow(effect['armor_slow'], effect['armor_slow_duration'])
        
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
    
    def resurrect(self):
        """Resurrect the player with half health"""
        if self.is_alive:
            return False  # Already alive
            
        self.is_alive = True
        self.hp = self.max_hp * 0.5  # Revive with half health
        self.invincible_time = PLAYER_INVINCIBILITY_TIME  # Brief invincibility after resurrection
        
        return True
        
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
        
    def gain_xp(self, amount):
        """Gain experience points"""
        self.xp += amount
        # Note: Level up logic would be handled elsewhere if needed
        
    def draw(self, screen):
        """Draw the player"""
        if self.visible:
            screen.blit(self.image, self.rect)
            
        # Draw attack hitbox for debugging
        if self.is_attacking and self.hitbox:
            pygame.draw.rect(screen, YELLOW, self.hitbox, 2)
            
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
            
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