import pygame
import random
import math
from settings import *
from src.enemy import Enemy, FastEnemy, TankEnemy, Boss, MajorBoss, XPOrb, DamageNumber
from src.item import ItemManager

class GameManager:
    def __init__(self):
        self.current_wave = 1
        self.wave_active = False
        self.wave_break_timer = 0
        self.enemies = pygame.sprite.Group()
        self.xp_orbs = pygame.sprite.Group()
        self.damage_numbers = []  # List of floating damage numbers
        self.item_manager = ItemManager()  # Item system
        
        # Screen shake effect
        self.screen_shake_timer = 0
        self.screen_shake_intensity = 0
        
        # Game state
        self.game_state = GAME_STATE_MENU
        self.skill_selection_player = None
        
        # Wave management
        self.enemies_to_spawn = 0
        self.spawn_timer = 0
        self.spawn_interval = 1.0  # seconds between enemy spawns
        
        # Boss tracking
        self.boss_spawned = False
        self.major_boss_spawned = False
        
    def start_new_game(self):
        """Start a new game"""
        self.current_wave = 1
        self.wave_active = False
        self.wave_break_timer = WAVE_BREAK_TIME
        self.enemies.empty()
        self.xp_orbs.empty()
        self.game_state = GAME_STATE_PLAYING
        self.skill_selection_player = None
        self.boss_spawned = False
        self.major_boss_spawned = False
        
    def update(self, dt, players):
        """Update game manager"""
        if self.game_state != GAME_STATE_PLAYING:
            return
            
        # Store players reference for skill selection
        self._players = players
            
        # Update enemies
        self.enemies.update(dt, players)
        
        # Update XP orbs
        self.xp_orbs.update(dt, players)
        
        # Update items
        self.item_manager.update(dt)
        
        # Update damage numbers
        self.damage_numbers = [dn for dn in self.damage_numbers if not dn.update(dt)]
        
        # Update screen shake
        if self.screen_shake_timer > 0:
            self.screen_shake_timer -= dt
            if self.screen_shake_timer <= 0:
                self.screen_shake_intensity = 0
        
        # Handle XP orb pickup
        self.handle_xp_pickup(players)
        
        # Handle item pickup
        self.handle_item_pickup(players)
        
        # Handle enemy-player collisions
        self.handle_enemy_collisions(players)
        
        # Handle player attacks
        self.handle_player_attacks(players)
        
        # Handle enemy projectile collisions
        self.handle_enemy_projectile_collisions(players)
        
        # Check if all players are dead
        if all(not player.is_alive for player in players):
            self.game_state = GAME_STATE_GAME_OVER
            return
            
        # Wave management
        if not self.wave_active:
            # Wave break period
            self.wave_break_timer -= dt
            if self.wave_break_timer <= 0:
                self.start_wave()
        else:
            # Wave is active
            self.update_wave_spawning(dt)
            
            # Check if wave is complete
            if len(self.enemies) == 0 and self.enemies_to_spawn == 0:
                self.complete_wave()
                
    def start_wave(self):
        """Start a new wave"""
        self.wave_active = True
        self.boss_spawned = False
        self.major_boss_spawned = False
        
        # Calculate enemies to spawn
        base_count = WAVE_BASE_ENEMY_COUNT
        additional_count = (self.current_wave - 1) * WAVE_ENEMY_INCREASE
        self.enemies_to_spawn = base_count + additional_count
        
        # Check if this is a boss wave
        if self.current_wave % BOSS_WAVE_INTERVAL == 0:
            self.enemies_to_spawn += 1  # Add one more for the boss
            
        # Add one more enemy for the major boss that spawns at end of every wave
        self.enemies_to_spawn += 1
        
        self.spawn_timer = 0
        self.enemies_per_wave = self.enemies_to_spawn  # Store for ratio calculation
        
    def update_wave_spawning(self, dt):
        """Handle enemy spawning during wave"""
        if self.enemies_to_spawn <= 0:
            return
            
        self.spawn_timer += dt
        
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_enemy()
            self.enemies_to_spawn -= 1
            self.spawn_timer = 0
            
            # Adjust spawn interval for difficulty
            self.spawn_interval = max(0.3, 1.0 - (self.current_wave * 0.05))
            
    def spawn_enemy(self):
        """Spawn a single enemy"""
        # Choose spawn position (from edges of screen)
        edge = random.randint(0, 3)  # 0=top, 1=right, 2=bottom, 3=left
        
        if edge == 0:  # top
            x = random.randint(0, SCREEN_WIDTH)
            y = -ENEMY_SIZE
        elif edge == 1:  # right
            x = SCREEN_WIDTH + ENEMY_SIZE
            y = random.randint(0, SCREEN_HEIGHT)
        elif edge == 2:  # bottom
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + ENEMY_SIZE
        else:  # left
            x = -ENEMY_SIZE
            y = random.randint(0, SCREEN_HEIGHT)
            
        # Determine enemy type
        if (self.current_wave % BOSS_WAVE_INTERVAL == 0 and 
            self.enemies_to_spawn == 0 and not self.boss_spawned):
            # Spawn boss
            enemy = Boss(SCREEN_WIDTH // 2, -BOSS_SIZE, self.current_wave)
            self.boss_spawned = True
        elif (self.enemies_to_spawn == 1 and not self.major_boss_spawned):
            # Spawn major boss as the last enemy of every wave
            enemy = MajorBoss(SCREEN_WIDTH // 2, -BOSS_SIZE - 20, self.current_wave)
            self.major_boss_spawned = True
        else:
            # Spawn regular enemy with increased chance of TankEnemy towards end of wave
            remaining_ratio = self.enemies_to_spawn / max(1, self.enemies_per_wave)
            if remaining_ratio < 0.3:  # Last 30% of wave - more tank enemies
                enemy_type = random.choices(
                    [Enemy, FastEnemy, TankEnemy],
                    weights=[40, 20, 40],  # 40% normal, 20% fast, 40% tank
                    k=1
                )[0]
            else:
                enemy_type = random.choices(
                    [Enemy, FastEnemy, TankEnemy],
                    weights=[60, 25, 15],  # 60% normal, 25% fast, 15% tank
                    k=1
                )[0]
            
            enemy = enemy_type(x, y, self.current_wave)
            
        self.enemies.add(enemy)
        
    def complete_wave(self):
        """Complete the current wave"""
        self.wave_active = False
        self.current_wave += 1
        self.wave_break_timer = WAVE_BREAK_TIME
        
        # Resurrect dead players if at least one teammate survived
        if hasattr(self, '_players') and self._players:
            alive_players = [p for p in self._players if p.is_alive]
            dead_players = [p for p in self._players if not p.is_alive]
            
            # Only resurrect if there's at least one alive player and at least one dead player
            if len(alive_players) > 0 and len(dead_players) > 0:
                for dead_player in dead_players:
                    dead_player.resurrect()
        
    def handle_xp_pickup(self, players):
        """Handle XP orb pickup by players"""
        for orb in self.xp_orbs:
            for player in players:
                if player.is_alive and orb.rect.colliderect(player.rect):
                    # Player picks up XP
                    level_up = player.add_xp(orb.xp_value)
                    orb.kill()
                    
                    # Handle level up
                    if level_up:
                        self.trigger_skill_selection(player)
                    break
                    
        # Remove expired orbs
        for orb in self.xp_orbs:
            if orb.lifetime <= 0:
                orb.kill()
                
    def handle_item_pickup(self, players):
        """Handle item pickup by players"""
        for player in players:
            if not player.is_alive:
                continue
                
            picked_up_items = self.item_manager.check_player_pickup(player)
            # Items are automatically applied by the ItemManager
                
    def handle_enemy_collisions(self, players):
        """Handle collisions between enemies and players"""
        for enemy in self.enemies:
            for player in players:
                if player.is_alive and enemy.collides_with_player(player):
                    # Player takes damage
                    if player.take_damage(enemy.damage):
                        # Knockback effect (optional)
                        pass
                        
    def handle_player_attacks(self, players):
        """Handle player attacks against enemies"""
        for player in players:
            if not player.is_alive or not player.is_attacking or not player.hitbox:
                continue
                
            stats = player.get_effective_stats()
            
            # Check collision with enemies
            for enemy in self.enemies:
                if player.hitbox.colliderect(enemy.rect):
                    # Calculate damage
                    damage = stats['damage']
                    
                    # Apply critical hit
                    if random.random() < stats['crit_chance']:
                        damage *= stats['crit_multiplier']
                        
                    # Apply execute skill
                    if ('execute' in player.skills and 
                        enemy.hp / enemy.max_hp <= 0.2):
                        damage = enemy.hp  # Instant kill
                        
                    # Deal damage
                    enemy_died = enemy.take_damage(damage, player)
                    
                    # Apply status effects
                    if 'frost_touch' in player.skills:
                        enemy.apply_slow(0.5, 2.0)
                        
                    if 'stun_strike' in player.skills:
                        if random.random() < 0.2:
                            enemy.apply_stun(1.5)
                    
                    # Apply elemental effects
                    if 'flame_weapon' in player.skills:
                        effect = SKILLS['flame_weapon']['effect']
                        self.apply_burn_effect(enemy, effect['burn_damage'] * player.skills['flame_weapon'], effect['burn_duration'])
                    
                    if 'poison_blade' in player.skills:
                        effect = SKILLS['poison_blade']['effect']
                        self.apply_poison_effect(enemy, effect['poison_damage'] * player.skills['poison_blade'], 
                                               effect['poison_duration'], effect['poison_slow'])
                    
                    if 'lightning_strike' in player.skills:
                        effect = SKILLS['lightning_strike']['effect']
                        self.apply_chain_lightning(enemy, damage, effect['chain_range'], effect['chain_count'])
                    
                    # Spell echo effect
                    if 'spell_echo' in player.skills and random.random() < SKILLS['spell_echo']['effect']['echo_chance']:
                        # Repeat the attack after a short delay
                        player.spell_echo_last_attack = {'damage': damage, 'target': enemy, 'delay': 0.2}
                            
                    # Life steal
                    if stats['life_steal'] > 0:
                        heal_amount = damage * stats['life_steal']
                        player.heal(heal_amount)
                        
                    # Handle enemy death
                    if enemy_died:
                        self.handle_enemy_death(enemy, player)
                        
                        # Blood frenzy effect
                        if 'blood_frenzy' in player.skills:
                            player.blood_frenzy_stacks = min(5, player.blood_frenzy_stacks + 1)
                            player.blood_frenzy_timer = 10.0
                        
            # Check projectile attacks
            self.handle_projectile_collisions(player)
            
    def handle_projectile_collisions(self, player):
        """Handle projectile collisions with enemies"""
        if not hasattr(player, 'projectiles'):
            return
            
        stats = player.get_effective_stats()
        
        # Convert sprite group to list for safe iteration
        projectile_list = list(player.projectiles.sprites())
        
        for projectile in projectile_list:
            # Sort enemies by distance from projectile to hit the closest one first
            enemies_with_distance = []
            for enemy in self.enemies:
                dx = projectile.rect.centerx - enemy.rect.centerx
                dy = projectile.rect.centery - enemy.rect.centery
                distance = math.sqrt(dx*dx + dy*dy)
                enemies_with_distance.append((distance, enemy))
            
            # Sort by distance (closest first)
            enemies_with_distance.sort(key=lambda x: x[0])
            
            for distance, enemy in enemies_with_distance:
                if projectile.rect.colliderect(enemy.rect):
                    # Use projectile's damage directly (already calculated in player.py)
                    damage = projectile.damage
                    
                    # Apply critical hit
                    is_crit = random.random() < stats['crit_chance']
                    if is_crit:
                        damage *= stats['crit_multiplier']
                        
                    # Deal damage
                    enemy_died = enemy.take_damage(damage, player)
                    
                    # Create floating damage number
                    damage_color = YELLOW if is_crit else WHITE
                    damage_number = DamageNumber(enemy.rect.centerx, enemy.rect.top - 10, damage, damage_color)
                    self.damage_numbers.append(damage_number)
                    
                    # Add screen shake for impact feedback
                    shake_intensity = 2 if is_crit else 1
                    self.add_screen_shake(shake_intensity, 0.1)
                    
                    # Life steal
                    if stats['life_steal'] > 0:
                        heal_amount = damage * stats['life_steal']
                        player.heal(heal_amount)
                        
                    # Handle enemy death
                    if enemy_died:
                        self.handle_enemy_death(enemy, player)
                        
                    # Handle piercing
                    if hasattr(projectile, 'piercing') and projectile.piercing > 0:
                        projectile.piercing -= 1
                    else:
                        # Remove projectile from sprite group and kill it
                        player.projectiles.remove(projectile)
                        projectile.kill()
                        break
            

                        
    def handle_enemy_projectile_collisions(self, players):
        """Handle collisions between enemy projectiles and players"""
        for enemy in self.enemies:
            for projectile in enemy.projectiles[:]:
                for player in players:
                    if player.is_alive and projectile.collides_with_player(player):
                        # Player takes damage from projectile
                        if player.take_damage(projectile.damage):
                            pass  # Player took damage
                        
                        # Remove projectile after hit
                        enemy.projectiles.remove(projectile)
                        break
                        
    def handle_enemy_death(self, enemy, killer_player):
        """Handle enemy death and XP drop"""
        # Create XP orb
        xp_orb = XPOrb(enemy.rect.centerx, enemy.rect.centery, enemy.xp_reward)
        self.xp_orbs.add(xp_orb)
        
        # Drop item based on enemy type
        enemy_type = 'normal'
        if isinstance(enemy, Boss) or isinstance(enemy, MajorBoss):
            enemy_type = 'boss'
        elif isinstance(enemy, TankEnemy):
            enemy_type = 'tank'
        
        self.item_manager.drop_item_from_enemy(enemy.rect.centerx, enemy.rect.centery, enemy_type)
        
        # Remove enemy
        enemy.kill()
        
    def trigger_skill_selection(self, player):
        """Trigger skill selection for a player"""
        # Don't change game state - keep playing
        self.skill_selection_player = player
        
    def complete_skill_selection(self, selection_data):
        """Complete skill selection"""
        if selection_data and 'player_id' in selection_data and 'skill' in selection_data:
            # Find the player by ID
            for player in [p for p in getattr(self, '_players', []) if hasattr(p, 'player_id')]:
                if player.player_id == selection_data['player_id']:
                    player.add_skill(selection_data['skill'])
                    break
            
            # If this was the skill_selection_player, clear it
            if (self.skill_selection_player and 
                self.skill_selection_player.player_id == selection_data['player_id']):
                self.skill_selection_player = None
                
        return selection_data['player_id'] if selection_data else None
        
    def get_enemies_remaining(self):
        """Get number of enemies remaining in current wave"""
        return len(self.enemies) + self.enemies_to_spawn
        
    def is_wave_break(self):
        """Check if currently in wave break"""
        return not self.wave_active and self.game_state == GAME_STATE_PLAYING
        
    def get_wave_break_time_remaining(self):
        """Get remaining time in wave break"""
        return max(0, self.wave_break_timer)
        
    def draw_debug_info(self, screen, font):
        """Draw debug information"""
        debug_info = [
            f"Wave: {self.current_wave}",
            f"Enemies: {len(self.enemies)}",
            f"To Spawn: {self.enemies_to_spawn}",
            f"XP Orbs: {len(self.xp_orbs)}",
            f"State: {self.game_state}"
        ]
        
        y = SCREEN_HEIGHT - 150
        for info in debug_info:
            text_surface = font.render(info, True, WHITE)
            screen.blit(text_surface, (10, y))
            y += 20
            
    def add_screen_shake(self, intensity, duration):
        """Add screen shake effect"""
        self.screen_shake_intensity = max(self.screen_shake_intensity, intensity)
        self.screen_shake_timer = max(self.screen_shake_timer, duration)
        
    def get_screen_shake_offset(self):
        """Get current screen shake offset"""
        if self.screen_shake_timer <= 0:
            return (0, 0)
        
        import random
        shake_x = random.randint(-int(self.screen_shake_intensity), int(self.screen_shake_intensity))
        shake_y = random.randint(-int(self.screen_shake_intensity), int(self.screen_shake_intensity))
        return (shake_x, shake_y)
    
    def reset_game(self):
        """Reset game to initial state"""
        self.__init__()
        
    def apply_burn_effect(self, enemy, damage, duration):
        """Apply burn effect to enemy"""
        if hasattr(enemy, 'burn_damage'):
            enemy.burn_damage = damage
            enemy.burn_duration = duration
        
    def apply_poison_effect(self, enemy, damage, duration, slow_factor):
        """Apply poison effect to enemy"""
        if hasattr(enemy, 'poison_damage'):
            enemy.poison_damage = damage
            enemy.poison_duration = duration
            enemy.poison_slow = slow_factor
            
    def apply_chain_lightning(self, initial_enemy, damage, chain_range, chain_count):
        """Apply chain lightning effect"""
        current_enemy = initial_enemy
        chained_enemies = {initial_enemy}
        current_damage = damage
        
        for i in range(chain_count - 1):
            nearest_enemy = None
            nearest_distance = float('inf')
            
            for enemy in self.enemies:
                if enemy in chained_enemies or not enemy.is_alive:
                    continue
                    
                distance = math.sqrt(
                    (enemy.rect.centerx - current_enemy.rect.centerx) ** 2 +
                    (enemy.rect.centery - current_enemy.rect.centery) ** 2
                )
                
                if distance <= chain_range and distance < nearest_distance:
                    nearest_distance = distance
                    nearest_enemy = enemy
            
            if nearest_enemy:
                current_damage *= 0.8  # Reduce damage for each chain
                nearest_enemy.take_damage(current_damage)
                chained_enemies.add(nearest_enemy)
                current_enemy = nearest_enemy
            else:
                break


class ParticleSystem:
    """Simple particle system for visual effects"""
    def __init__(self):
        self.particles = []
        
    def add_blood_particles(self, x, y):
        """Add blood particles at position"""
        for _ in range(BLOOD_PARTICLE_COUNT):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-50, 50),
                'vy': random.uniform(-50, 50),
                'lifetime': PARTICLE_LIFETIME,
                'color': RED,
                'size': random.randint(2, 4)
            }
            self.particles.append(particle)
            
    def add_xp_particles(self, x, y):
        """Add XP particles at position"""
        for _ in range(3):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-30, 30),
                'vy': random.uniform(-30, 30),
                'lifetime': PARTICLE_LIFETIME * 0.5,
                'color': YELLOW,
                'size': random.randint(1, 3)
            }
            self.particles.append(particle)
            
    def update(self, dt):
        """Update all particles"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['lifetime'] -= dt
            
            # Apply gravity
            particle['vy'] += 100 * dt
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
                
    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            alpha = int(255 * (particle['lifetime'] / PARTICLE_LIFETIME))
            color = (*particle['color'][:3], alpha)
            
            # Create surface with alpha
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
            particle_surface.set_alpha(alpha)
            particle_surface.fill(particle['color'])
            
            screen.blit(particle_surface, 
                       (int(particle['x'] - particle['size']), 
                        int(particle['y'] - particle['size'])))