import pygame
import random
import math
from settings import *

class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.item_data = ITEMS[item_type]
        
        # Visual properties
        self.size = 12
        self.color = self.item_data['color']
        self.bounce_offset = 0
        self.bounce_timer = 0
        
        # Lifetime
        self.lifetime = ITEM_LIFETIME
        self.blink_timer = 0
        self.visible = True
        
        # Physics
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-3, -1)
        self.friction = 0.95
        
        # Pickup properties
        self.pickup_range = ITEM_PICKUP_RANGE
        self.collected = False
        
    def update(self, dt):
        """Update item state"""
        if self.collected:
            return
            
        # Update lifetime
        self.lifetime -= dt
        
        # Blink when about to expire
        if self.lifetime < 5.0:
            self.blink_timer += dt
            if self.blink_timer > 0.2:
                self.visible = not self.visible
                self.blink_timer = 0
        
        # Remove if expired
        if self.lifetime <= 0:
            self.collected = True
            return
            
        # Update physics
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Apply friction
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # Bounce animation
        self.bounce_timer += dt * ITEM_BOUNCE_SPEED
        self.bounce_offset = math.sin(self.bounce_timer) * ITEM_BOUNCE_HEIGHT
        
    def draw(self, screen, camera_x, camera_y):
        """Draw the item"""
        if self.collected or not self.visible:
            return
            
        # Calculate screen position
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y + self.bounce_offset
        
        # Don't draw if off screen
        if (screen_x < -50 or screen_x > SCREEN_WIDTH + 50 or 
            screen_y < -50 or screen_y > SCREEN_HEIGHT + 50):
            return
            
        # Draw item based on rarity
        rarity = self.item_data['rarity']
        
        # Draw glow effect for rare items
        if rarity in ['rare', 'epic', 'legendary']:
            glow_size = self.size + 4
            glow_color = (*self.color, 100)  # Semi-transparent
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), glow_size)
            screen.blit(glow_surface, (screen_x - glow_size, screen_y - glow_size))
        
        # Draw main item
        if self.item_data['type'] == 'consumable':
            # Draw as circle for consumables
            pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.size)
            pygame.draw.circle(screen, (255, 255, 255), (int(screen_x), int(screen_y)), self.size, 2)
        elif self.item_data['type'] == 'permanent':
            # Draw as diamond for permanent upgrades
            points = [
                (screen_x, screen_y - self.size),
                (screen_x + self.size, screen_y),
                (screen_x, screen_y + self.size),
                (screen_x - self.size, screen_y)
            ]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
        elif self.item_data['type'] == 'buff':
            # Draw as hexagon for buffs
            points = []
            for i in range(6):
                angle = i * math.pi / 3
                px = screen_x + self.size * math.cos(angle)
                py = screen_y + self.size * math.sin(angle)
                points.append((px, py))
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
        else:
            # Draw as star for special items
            self._draw_star(screen, screen_x, screen_y, self.size)
            
    def _draw_star(self, screen, x, y, size):
        """Draw a star shape"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size * 0.5
            px = x + radius * math.cos(angle - math.pi / 2)
            py = y + radius * math.sin(angle - math.pi / 2)
            points.append((px, py))
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)
        
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                          self.size * 2, self.size * 2)
                          
    def is_near_player(self, player_x, player_y):
        """Check if item is within pickup range of player"""
        distance = math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)
        return distance <= self.pickup_range
        
    def collect(self):
        """Mark item as collected"""
        self.collected = True
        
class ItemManager:
    def __init__(self):
        self.items = []
        
    def add_item(self, x, y, item_type=None):
        """Add a new item at the specified position"""
        if item_type is None:
            item_type = self._get_random_item_type()
        
        item = Item(x, y, item_type)
        self.items.append(item)
        return item
        
    def _get_random_item_type(self):
        """Get a random item type based on rarity weights"""
        # Create weighted list based on drop rates
        weighted_items = []
        for item_type, item_data in ITEMS.items():
            rarity = item_data['rarity']
            weight = ITEM_DROP_RATES.get(rarity, 0.01)
            # Add item multiple times based on weight (multiply by 1000 for precision)
            count = int(weight * 1000)
            weighted_items.extend([item_type] * count)
        
        return random.choice(weighted_items) if weighted_items else 'health_potion'
        
    def drop_item_from_enemy(self, enemy_x, enemy_y, enemy_type='normal'):
        """Drop an item when an enemy dies"""
        # Base drop chance
        base_drop_chance = 0.3  # 30% base chance
        
        # Modify drop chance based on enemy type
        if enemy_type == 'boss':
            drop_chance = 0.8  # 80% for bosses
        elif enemy_type == 'tank':
            drop_chance = 0.5  # 50% for tank enemies
        else:
            drop_chance = base_drop_chance
            
        if random.random() < drop_chance:
            # Add some randomness to drop position
            drop_x = enemy_x + random.uniform(-20, 20)
            drop_y = enemy_y + random.uniform(-20, 20)
            return self.add_item(drop_x, drop_y)
        return None
        
    def update(self, dt):
        """Update all items"""
        # Update items and remove collected/expired ones
        self.items = [item for item in self.items if not item.collected]
        
        for item in self.items:
            item.update(dt)
            
    def draw(self, screen, camera_x, camera_y):
        """Draw all items"""
        for item in self.items:
            item.draw(screen, camera_x, camera_y)
            
    def check_player_pickup(self, player):
        """Check if player can pick up any items"""
        picked_up_items = []
        
        for item in self.items[:]:
            if item.is_near_player(player.rect.centerx, player.rect.centery):
                # Apply item effect to player
                self._apply_item_effect(player, item)
                item.collect()
                picked_up_items.append(item)
                
        return picked_up_items
        
    def _apply_item_effect(self, player, item):
        """Apply item effect to the player"""
        effect = item.item_data['effect']
        
        # Healing effects
        if 'heal' in effect:
            player.heal(effect['heal'])
            
        # Mana effects
        if 'mana' in effect:
            player.mana = min(player.max_mana, player.mana + effect['mana'])
            
        # XP effects
        if 'xp' in effect:
            player.gain_xp(effect['xp'])
            
        # Permanent upgrades
        if 'max_hp_increase' in effect:
            player.max_hp += effect['max_hp_increase']
            player.hp += effect['max_hp_increase']  # Also heal
            
        if 'damage_increase' in effect:
            player.base_damage *= (1 + effect['damage_increase'])
            
        if 'speed_increase' in effect:
            player.base_speed *= (1 + effect['speed_increase'])
            
        # Temporary buffs
        if 'damage_boost' in effect:
            player.damage_boost_timer = effect['duration']
            player.damage_boost_multiplier = 1 + effect['damage_boost']
            
        if 'speed_boost' in effect:
            player.speed_boost_timer = effect['duration']
            player.speed_boost_multiplier = 1 + effect['speed_boost']
            
        if 'crit_boost' in effect:
            player.crit_boost_timer = effect['duration']
            player.crit_boost_amount = effect['crit_boost']
            
        if 'invincible' in effect:
            player.invincible_timer = effect['duration']
            
        if 'explosive_attacks' in effect:
            player.explosive_attacks_remaining = effect['explosive_attacks']
            
        # Special effects
        if 'random_skill' in effect:
            # This would need to be implemented in the skill system
            pass
            
        if 'revive' in effect:
            player.has_phoenix_feather = True
            
    def clear_all_items(self):
        """Remove all items"""
        self.items.clear()
        
    def get_item_count(self):
        """Get total number of items"""
        return len(self.items)