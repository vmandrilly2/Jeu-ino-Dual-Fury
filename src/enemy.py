import pygame
import math
import random
from settings import *

class DamageNumber(pygame.sprite.Sprite):
    """Floating damage number that appears when enemies take damage"""
    def __init__(self, x, y, damage, color=WHITE):
        super().__init__()
        
        # Create text surface
        font = pygame.font.Font(None, 24)
        self.image = font.render(str(int(damage)), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Animation properties
        self.velocity_y = -50  # Move upward
        self.lifetime = 1.0  # Duration in seconds
        self.alpha = 255
        
    def update(self, dt):
        """Update damage number animation"""
        # Move upward
        self.rect.y += self.velocity_y * dt
        
        # Fade out
        self.lifetime -= dt
        self.alpha = max(0, int(255 * (self.lifetime / 1.0)))
        
        # Update alpha
        self.image.set_alpha(self.alpha)
        
        # Remove when lifetime expires
        if self.lifetime <= 0:
            return True  # Should be removed
        return False
        
    def draw(self, screen):
        """Draw damage number"""
        screen.blit(self.image, self.rect)

class Projectile(pygame.sprite.Sprite):
    """Projectile fired by enemies"""
    def __init__(self, x, y, target_x, target_y, speed=PROJECTILE_SPEED, damage=10, color=RED):
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
            self.velocity = pygame.math.Vector2(
                (dx / distance) * speed,
                (dy / distance) * speed
            )
        else:
            self.velocity = pygame.math.Vector2(0, 0)
            
        self.damage = damage
        self.lifetime = 5.0  # Disappear after 5 seconds
        
    def update(self, dt):
        """Update projectile position"""
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
        
        self.lifetime -= dt
        
        # Remove if out of bounds or lifetime expired
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.lifetime <= 0):
            return True  # Should be removed
            
        return False
        
    def draw(self, screen):
        """Draw projectile"""
        screen.blit(self.image, self.rect)
        
    def collides_with_player(self, player):
        """Check collision with player"""
        return self.rect.colliderect(player.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, wave_number=1):
        super().__init__()
        
        # Create enemy sprite
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Base stats
        self.base_hp = ENEMY_BASE_HP
        self.base_speed = ENEMY_BASE_SPEED
        self.base_damage = ENEMY_BASE_DAMAGE
        
        # Scale stats based on wave
        self.max_hp = self.base_hp + (wave_number - 1) * ENEMY_HP_SCALING
        self.hp = self.max_hp
        self.speed = self.base_speed
        self.damage = self.base_damage + (wave_number - 1) * ENEMY_DAMAGE_SCALING
        self.xp_reward = ENEMY_XP_REWARD
        
        # Shooting mechanics
        self.can_shoot = False
        self.shoot_timer = 0
        self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN
        self.projectiles = []
        
        # Movement and AI
        self.velocity = pygame.math.Vector2(0, 0)
        self.target_player = None
        
        # Status effects
        self.slow_timer = 0
        self.slow_factor = 1.0
        self.stun_timer = 0
        self.is_stunned = False
        
        # Visual effects
        self.flash_timer = 0
        self.flash_duration = 0
        
    def update(self, dt, players):
        """Update enemy state"""
        # Update status effects
        self.slow_timer = max(0, self.slow_timer - dt)
        if self.slow_timer <= 0:
            self.slow_factor = 1.0
            
        self.stun_timer = max(0, self.stun_timer - dt)
        if self.stun_timer <= 0:
            self.is_stunned = False
            
        self.flash_timer = max(0, self.flash_timer - dt)
        
        # Update projectiles
        self.projectiles = [p for p in self.projectiles if not p.update(dt)]
        
        # Don't move if stunned
        if self.is_stunned:
            return
            
        # Find closest living player
        self.target_player = self.find_closest_player(players)
        
        if self.target_player:
            self.move_towards_target(dt)
            
            # Handle shooting
            if self.can_shoot:
                self.shoot_timer += dt
                if self.shoot_timer >= self.shoot_cooldown:
                    self.shoot_at_player()
                    self.shoot_timer = 0
            
    def find_closest_player(self, players):
        """Find the closest living player"""
        closest_player = None
        closest_distance = float('inf')
        
        for player in players:
            if player.is_alive:
                distance = self.distance_to_player(player)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_player = player
                    
        return closest_player
        
    def distance_to_player(self, player):
        """Calculate distance to a player"""
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        return math.sqrt(dx * dx + dy * dy)
        
    def move_towards_target(self, dt):
        """Move towards the target player"""
        if not self.target_player:
            return
            
        # Calculate direction to target
        dx = self.target_player.rect.centerx - self.rect.centerx
        dy = self.target_player.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Apply speed and slow factor
            effective_speed = self.speed * self.slow_factor
            
            # Update velocity
            self.velocity.x = dx * effective_speed
            self.velocity.y = dy * effective_speed
            
            # Update position
            self.rect.x += self.velocity.x * dt
            self.rect.y += self.velocity.y * dt
            
    def take_damage(self, damage, player=None):
        """Take damage and return True if enemy dies"""
        self.hp -= damage
        
        # Visual feedback
        self.flash_timer = 0.1
        self.flash_duration = 0.1
        
        if self.hp <= 0:
            return True  # Enemy is dead
            
        return False
        
    def apply_slow(self, slow_factor, duration):
        """Apply slow effect"""
        self.slow_factor = slow_factor
        self.slow_timer = duration
        
    def apply_stun(self, duration):
        """Apply stun effect"""
        self.is_stunned = True
        self.stun_timer = duration
        
    def shoot_at_player(self):
        """Shoot a projectile at the target player"""
        if self.target_player:
            projectile = Projectile(
                self.rect.centerx, self.rect.centery,
                self.target_player.rect.centerx, self.target_player.rect.centery,
                damage=self.damage // 2  # Projectile damage is half of melee damage
            )
            self.projectiles.append(projectile)
        
    def draw(self, screen):
        """Draw the enemy"""
        # Flash white when taking damage
        if self.flash_timer > 0:
            flash_surface = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
            flash_surface.fill(WHITE)
            screen.blit(flash_surface, self.rect)
        else:
            screen.blit(self.image, self.rect)
            
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
            
        # Draw health bar
        if self.hp < self.max_hp:
            bar_width = ENEMY_SIZE
            bar_height = 4
            bar_x = self.rect.x
            bar_y = self.rect.y - 8
            
            # Background
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            
            # Health
            health_width = int((self.hp / self.max_hp) * bar_width)
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
            
    def get_center(self):
        """Get enemy center position"""
        return self.rect.center
        
    def collides_with_player(self, player):
        """Check collision with player"""
        return self.rect.colliderect(player.rect)


class FastEnemy(Enemy):
    """Fast but weak enemy"""
    def __init__(self, x, y, wave_number=1):
        super().__init__(x, y, wave_number)
        
        # Modify stats for fast enemy
        self.speed = self.base_speed * 1.5
        self.max_hp = int(self.base_hp * 0.7) + (wave_number - 1) * ENEMY_HP_SCALING
        self.hp = self.max_hp
        self.damage = int((self.base_damage + (wave_number - 1) * ENEMY_DAMAGE_SCALING) * 0.8)
        
        # Enable shooting for fast enemies
        self.can_shoot = True
        self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN * 0.8  # Faster shooting
        
        # Different color
        self.image.fill(ORANGE)
        

class TankEnemy(Enemy):
    """Violet semi-boss enemy with multi-directional shooting"""
    def __init__(self, x, y, wave_number=1):
        super().__init__(x, y, wave_number)
        
        # Modify stats for tank enemy - now faster and tankier
        self.speed = self.base_speed * 1.2  # Increased from 0.6 to 1.2
        self.max_hp = int(self.base_hp * 3.0) + (wave_number - 1) * ENEMY_HP_SCALING * 2  # Increased from 1.5 to 3.0
        self.hp = self.max_hp
        self.damage = int((self.base_damage + (wave_number - 1) * ENEMY_DAMAGE_SCALING) * 1.5)
        self.xp_reward = ENEMY_XP_REWARD * 3  # More XP since tankier
        
        # Enable shooting with multi-directional pattern
        self.can_shoot = True
        self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN * 1.2  # Slightly slower than fast enemies
        self.multi_shot_timer = 0
        self.multi_shot_cooldown = 4.0  # Multi-directional shot every 4 seconds
        
        # Different color and size
        self.image = pygame.Surface((ENEMY_SIZE + 12, ENEMY_SIZE + 12))  # Larger size
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self, dt, players):
        """Update tank enemy with multi-directional shooting"""
        super().update(dt, players)
        
        # Handle multi-directional shooting
        self.multi_shot_timer += dt
        if self.multi_shot_timer >= self.multi_shot_cooldown:
            self.perform_multi_shot()
            self.multi_shot_timer = 0
    
    def perform_multi_shot(self):
        """Perform multi-directional shooting attack"""
        # Shoot in 6 directions
        num_directions = 6
        for i in range(num_directions):
            angle = (i / num_directions) * 2 * math.pi
            target_x = self.rect.centerx + math.cos(angle) * 150
            target_y = self.rect.centery + math.sin(angle) * 150
            
            projectile = Projectile(
                self.rect.centerx, self.rect.centery,
                target_x, target_y,
                speed=PROJECTILE_SPEED * 0.9,
                damage=self.damage // 3,  # Lower damage since multiple projectiles
                color=PURPLE  # Purple projectiles for tank enemies
            )
            self.projectiles.append(projectile)
        

class HomingProjectile(Projectile):
    """Projectile that follows the closest player"""
    def __init__(self, x, y, target_x, target_y, speed=PROJECTILE_SPEED, damage=10, color=RED, homing_strength=0.3):
        super().__init__(x, y, target_x, target_y, speed, damage, color)
        self.homing_strength = homing_strength
        self.target_player = None
        
    def update(self, dt, players=None):
        """Update homing projectile with player tracking"""
        if players:
            # Find closest living player
            closest_player = None
            closest_distance = float('inf')
            
            for player in players:
                if player.is_alive:
                    distance = math.sqrt(
                        (player.rect.centerx - self.rect.centerx) ** 2 +
                        (player.rect.centery - self.rect.centery) ** 2
                    )
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_player = player
            
            # Adjust velocity towards closest player
            if closest_player:
                dx = closest_player.rect.centerx - self.rect.centerx
                dy = closest_player.rect.centery - self.rect.centery
                distance = math.sqrt(dx * dx + dy * dy)
                
                if distance > 0:
                    # Blend current velocity with homing direction
                    target_vel_x = (dx / distance) * self.velocity.length()
                    target_vel_y = (dy / distance) * self.velocity.length()
                    
                    self.velocity.x += (target_vel_x - self.velocity.x) * self.homing_strength * dt
                    self.velocity.y += (target_vel_y - self.velocity.y) * self.homing_strength * dt
        
        # Call parent update
        return super().update(dt)

class LargeProjectile(Projectile):
    """Larger, slower projectile with more damage"""
    def __init__(self, x, y, target_x, target_y, speed=PROJECTILE_SPEED, damage=20, color=RED):
        super().__init__(x, y, target_x, target_y, speed * 0.7, damage, color)  # 30% slower
        
        # Make it larger
        self.image = pygame.Surface((PROJECTILE_SIZE * 2, PROJECTILE_SIZE * 2))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Boss(Enemy):
    """Boss enemy with special abilities"""
    def __init__(self, x, y, wave_number=1):
        super().__init__(x, y, wave_number)
        
        # Boss stats
        self.max_hp = BOSS_BASE_HP + (wave_number - 1) * 100
        self.hp = self.max_hp
        self.speed = BOSS_SPEED
        self.damage = BOSS_DAMAGE + (wave_number - 1) * ENEMY_DAMAGE_SCALING * 2
        self.xp_reward = BOSS_XP_REWARD
        
        # Boss appearance
        self.image = pygame.Surface((BOSS_SIZE, BOSS_SIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Boss shooting abilities
        self.can_shoot = True
        self.shoot_cooldown = BOSS_SHOOT_COOLDOWN
        self.special_attack_timer = 0
        self.special_attack_cooldown = BOSS_SPECIAL_ATTACK_COOLDOWN
        
        # Boss abilities
        self.charge_timer = 0
        self.charge_cooldown = 3.0
        self.is_charging = False
        self.charge_target = None
        
    def update(self, dt, players):
        """Update boss with special abilities"""
        super().update(dt, players)
        
        # Handle special attacks
        self.special_attack_timer += dt
        
        # Special area attack every few seconds
        if self.special_attack_timer >= self.special_attack_cooldown:
            self.perform_special_attack(players)
            self.special_attack_timer = 0
        
        # Handle charge attack
        self.charge_timer += dt
        
        if self.charge_timer >= self.charge_cooldown and not self.is_charging:
            if self.target_player:
                self.start_charge_attack()
                
        if self.is_charging:
            self.handle_charge_attack(dt)
            
    def start_charge_attack(self):
        """Start a charge attack towards the target"""
        self.is_charging = True
        self.charge_target = self.target_player.rect.center
        self.charge_timer = 0
        
        # Calculate charge direction
        dx = self.charge_target[0] - self.rect.centerx
        dy = self.charge_target[1] - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            self.charge_velocity = pygame.math.Vector2(
                (dx / distance) * self.speed * 3,
                (dy / distance) * self.speed * 3
            )
        else:
            self.charge_velocity = pygame.math.Vector2(0, 0)
            
    def handle_charge_attack(self, dt):
        """Handle the charge attack movement"""
        # Move with charge velocity
        self.rect.x += self.charge_velocity.x * dt
        self.rect.y += self.charge_velocity.y * dt
        
        # Stop charging after 1 second or if hit wall
        if (self.charge_timer >= 1.0 or 
            self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH or
            self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT):
            
            self.is_charging = False
            self.charge_timer = 0
            
    def perform_special_attack(self, players):
        """Perform special area coverage attack"""
        # Spiral shot pattern
        num_projectiles = 8
        for i in range(num_projectiles):
            angle = (i / num_projectiles) * 2 * math.pi
            target_x = self.rect.centerx + math.cos(angle) * 200
            target_y = self.rect.centery + math.sin(angle) * 200
            
            projectile = Projectile(
                self.rect.centerx, self.rect.centery,
                target_x, target_y,
                speed=PROJECTILE_SPEED * 0.8,
                damage=self.damage // 3,
                color=YELLOW  # Boss projectiles are yellow
            )
            self.projectiles.append(projectile)
            
        # Additional targeted shots at players
        for player in players:
            if player.is_alive:
                projectile = Projectile(
                    self.rect.centerx, self.rect.centery,
                    player.rect.centerx, player.rect.centery,
                    speed=PROJECTILE_SPEED * 1.2,
                    damage=self.damage // 2,
                    color=YELLOW
                )
                self.projectiles.append(projectile)
            
    def draw(self, screen):
        """Draw the boss with special effects"""
        # Draw boss with pulsing effect
        if self.is_charging:
            # Draw charging effect
            charge_surface = pygame.Surface((BOSS_SIZE + 10, BOSS_SIZE + 10))
            charge_surface.fill(YELLOW)
            charge_rect = charge_surface.get_rect(center=self.rect.center)
            screen.blit(charge_surface, charge_rect)
            
        # Flash white when taking damage (correct size for boss)
        if self.flash_timer > 0:
            flash_surface = pygame.Surface((BOSS_SIZE, BOSS_SIZE))
            flash_surface.fill(WHITE)
            screen.blit(flash_surface, self.rect)
        else:
            screen.blit(self.image, self.rect)
            
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
        
        # Draw boss health bar (larger)
        bar_width = BOSS_SIZE
        bar_height = 8
        bar_x = self.rect.x
        bar_y = self.rect.y - 15
        
        # Background
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_width = int((self.hp / self.max_hp) * bar_width)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        
        # Draw boss name
        font = pygame.font.Font(None, 24)
        text = font.render("BOSS", True, WHITE)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.y - 25))
        screen.blit(text, text_rect)


class MajorBoss(Enemy):
    """Major boss that appears at the end of each wave with special projectiles"""
    def __init__(self, x, y, wave_number=1):
        super().__init__(x, y, wave_number)
        
        # Major boss stats - stronger than regular boss
        self.max_hp = BOSS_BASE_HP * 1.5 + (wave_number - 1) * 150
        self.hp = self.max_hp
        self.speed = BOSS_SPEED * 0.8  # Slightly slower but more dangerous
        self.damage = BOSS_DAMAGE * 1.5 + (wave_number - 1) * ENEMY_DAMAGE_SCALING * 3
        self.xp_reward = BOSS_XP_REWARD * 2
        
        # Major boss appearance - larger and different color
        self.image = pygame.Surface((BOSS_SIZE + 20, BOSS_SIZE + 20))
        self.image.fill((128, 0, 64))  # Dark purple
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Special shooting abilities
        self.can_shoot = True
        self.shoot_cooldown = BOSS_SHOOT_COOLDOWN * 0.8
        self.homing_attack_timer = 0
        self.homing_attack_cooldown = 6.0
        self.large_shot_timer = 0
        self.large_shot_cooldown = 4.0
        self.spiral_attack_timer = 0
        self.spiral_attack_cooldown = 8.0
        
    def update(self, dt, players):
        """Update major boss with special attacks"""
        super().update(dt, players)
        
        # Handle homing attack
        self.homing_attack_timer += dt
        if self.homing_attack_timer >= self.homing_attack_cooldown:
            self.perform_homing_attack(players)
            self.homing_attack_timer = 0
            
        # Handle large shot attack
        self.large_shot_timer += dt
        if self.large_shot_timer >= self.large_shot_cooldown:
            self.perform_large_shot_attack(players)
            self.large_shot_timer = 0
            
        # Handle spiral attack
        self.spiral_attack_timer += dt
        if self.spiral_attack_timer >= self.spiral_attack_cooldown:
            self.perform_spiral_attack()
            self.spiral_attack_timer = 0
    
    def perform_homing_attack(self, players):
        """Launch homing projectiles at players"""
        for player in players:
            if player.is_alive:
                projectile = HomingProjectile(
                    self.rect.centerx, self.rect.centery,
                    player.rect.centerx, player.rect.centery,
                    speed=PROJECTILE_SPEED * 0.8,
                    damage=self.damage // 2,
                    color=(255, 100, 100),  # Light red for homing
                    homing_strength=0.5
                )
                self.projectiles.append(projectile)
    
    def perform_large_shot_attack(self, players):
        """Launch large projectiles in multiple directions"""
        num_shots = 4
        for i in range(num_shots):
            angle = (i / num_shots) * 2 * math.pi
            target_x = self.rect.centerx + math.cos(angle) * 200
            target_y = self.rect.centery + math.sin(angle) * 200
            
            projectile = LargeProjectile(
                self.rect.centerx, self.rect.centery,
                target_x, target_y,
                speed=PROJECTILE_SPEED,
                damage=self.damage // 2,
                color=(255, 200, 0)  # Orange for large shots
            )
            self.projectiles.append(projectile)
    
    def perform_spiral_attack(self):
        """Launch a spiral pattern of projectiles"""
        num_projectiles = 12
        for i in range(num_projectiles):
            angle = (i / num_projectiles) * 2 * math.pi
            target_x = self.rect.centerx + math.cos(angle) * 180
            target_y = self.rect.centery + math.sin(angle) * 180
            
            projectile = Projectile(
                self.rect.centerx, self.rect.centery,
                target_x, target_y,
                speed=PROJECTILE_SPEED * 0.9,
                damage=self.damage // 4,
                color=(200, 0, 200)  # Purple for spiral
            )
            self.projectiles.append(projectile)
    
    def draw(self, screen):
        """Draw the major boss with special effects"""
        # Flash white when taking damage (correct size for major boss)
        if self.flash_timer > 0:
            flash_surface = pygame.Surface((BOSS_SIZE + 20, BOSS_SIZE + 20))
            flash_surface.fill(WHITE)
            screen.blit(flash_surface, self.rect)
        else:
            screen.blit(self.image, self.rect)
            
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
        
        # Draw major boss health bar (even larger)
        bar_width = BOSS_SIZE + 20
        bar_height = 10
        bar_x = self.rect.x
        bar_y = self.rect.y - 20
        
        # Background
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_width = int((self.hp / self.max_hp) * bar_width)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        
        # Major boss name
        font = pygame.font.Font(None, 28)
        text = font.render("MAJOR BOSS", True, WHITE)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.y - 35))
        screen.blit(text, text_rect)


class XPOrb(pygame.sprite.Sprite):
    """Experience orb dropped by enemies"""
    def __init__(self, x, y, xp_value):
        super().__init__()
        
        self.image = pygame.Surface((8, 8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.xp_value = xp_value
        self.lifetime = 10.0  # Disappear after 10 seconds
        self.pickup_range = 30
        
        # Movement towards player
        self.velocity = pygame.math.Vector2(0, 0)
        self.attracted_to_player = None
        
    def update(self, dt, players):
        """Update XP orb"""
        self.lifetime -= dt
        
        # Find closest player for attraction
        closest_player = None
        closest_distance = float('inf')
        
        for player in players:
            if player.is_alive:
                distance = self.distance_to_player(player)
                pickup_range = self.pickup_range
                
                # Increase pickup range if player has magnet skill
                if 'magnet' in player.skills:
                    pickup_range *= (1 + 0.5 * player.skills['magnet'])
                    
                if distance < pickup_range and distance < closest_distance:
                    closest_distance = distance
                    closest_player = player
                    
        # Move towards closest player
        if closest_player:
            dx = closest_player.rect.centerx - self.rect.centerx
            dy = closest_player.rect.centery - self.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance > 0:
                speed = 200  # XP orb movement speed
                self.velocity.x = (dx / distance) * speed
                self.velocity.y = (dy / distance) * speed
                
                self.rect.x += self.velocity.x * dt
                self.rect.y += self.velocity.y * dt
                
    def distance_to_player(self, player):
        """Calculate distance to player"""
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        return math.sqrt(dx * dx + dy * dy)
        
    def draw(self, screen):
        """Draw XP orb"""
        screen.blit(self.image, self.rect)