import pygame
import math
import random
from settings import *

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
        self.damage = self.base_damage
        self.xp_reward = ENEMY_XP_REWARD
        
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
        
        # Don't move if stunned
        if self.is_stunned:
            return
            
        # Find closest living player
        self.target_player = self.find_closest_player(players)
        
        if self.target_player:
            self.move_towards_target(dt)
            
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
        
    def draw(self, screen):
        """Draw the enemy"""
        # Flash white when taking damage
        if self.flash_timer > 0:
            flash_surface = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
            flash_surface.fill(WHITE)
            screen.blit(flash_surface, self.rect)
        else:
            screen.blit(self.image, self.rect)
            
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
        self.damage = int(self.base_damage * 0.8)
        
        # Different color
        self.image.fill(ORANGE)
        

class TankEnemy(Enemy):
    """Slow but strong enemy"""
    def __init__(self, x, y, wave_number=1):
        super().__init__(x, y, wave_number)
        
        # Modify stats for tank enemy
        self.speed = self.base_speed * 0.6
        self.max_hp = int(self.base_hp * 1.5) + (wave_number - 1) * ENEMY_HP_SCALING
        self.hp = self.max_hp
        self.damage = int(self.base_damage * 1.3)
        
        # Different color and size
        self.image = pygame.Surface((ENEMY_SIZE + 8, ENEMY_SIZE + 8))
        self.image.fill(PURPLE)
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
        self.damage = BOSS_DAMAGE
        self.xp_reward = BOSS_XP_REWARD
        
        # Boss appearance
        self.image = pygame.Surface((BOSS_SIZE, BOSS_SIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Boss abilities
        self.charge_timer = 0
        self.charge_cooldown = 3.0
        self.is_charging = False
        self.charge_target = None
        
    def update(self, dt, players):
        """Update boss with special abilities"""
        super().update(dt, players)
        
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
            
    def draw(self, screen):
        """Draw the boss with special effects"""
        # Draw boss with pulsing effect
        if self.is_charging:
            # Draw charging effect
            charge_surface = pygame.Surface((BOSS_SIZE + 10, BOSS_SIZE + 10))
            charge_surface.fill(YELLOW)
            charge_rect = charge_surface.get_rect(center=self.rect.center)
            screen.blit(charge_surface, charge_rect)
            
        super().draw(screen)
        
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
        
        # Boss name
        font = pygame.font.Font(None, 24)
        text = font.render("BOSS", True, WHITE)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.y - 25))
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