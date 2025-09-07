import pygame
import random
from settings import *

def get_text(key):
    """Get translated text based on current language"""
    return TRANSLATIONS[CURRENT_LANGUAGE].get(key, key)

def get_skill_name(skill_key):
    """Get translated skill name"""
    skill = SKILLS.get(skill_key, {})
    if CURRENT_LANGUAGE == 'zh' and 'name_zh' in skill:
        return skill['name_zh']
    return skill.get('name', skill_key)

def get_skill_description(skill_key):
    """Get translated skill description"""
    skill = SKILLS.get(skill_key, {})
    if CURRENT_LANGUAGE == 'zh' and 'description_zh' in skill:
        return skill['description_zh']
    return skill.get('description', '')

class UI:
    def __init__(self):
        # Try to use a system font that supports Chinese characters
        try:
            self.font = pygame.font.SysFont('simsun,arial,helvetica', UI_FONT_SIZE)
            self.small_font = pygame.font.SysFont('simsun,arial,helvetica', UI_SMALL_FONT_SIZE)
            self.large_font = pygame.font.SysFont('simsun,arial,helvetica', UI_LARGE_FONT_SIZE)
        except:
            # Fallback to default font
            self.font = pygame.font.Font(None, UI_FONT_SIZE)
            self.small_font = pygame.font.Font(None, UI_SMALL_FONT_SIZE)
            self.large_font = pygame.font.Font(None, UI_LARGE_FONT_SIZE)
        
    def draw_player_hud(self, screen, player, position='left'):
        """Draw HUD for a player (health, XP, level)"""
        if position == 'left':
            x = UI_MARGIN
            y = UI_MARGIN
        else:  # right
            x = SCREEN_WIDTH - UI_MARGIN - HEALTH_BAR_WIDTH
            y = UI_MARGIN
            
        # Player label
        label = f"{get_text('player')} {player.player_id}"
        label_surface = self.font.render(label, True, WHITE)
        screen.blit(label_surface, (x, y))
        y += 30
        
        # Health bar
        self.draw_health_bar(screen, player, x, y)
        y += 30
        
        # XP bar
        self.draw_xp_bar(screen, player, x, y)
        y += 30
        
        # Level
        level_text = f"{get_text('level')}: {player.level}"
        level_surface = self.font.render(level_text, True, WHITE)
        screen.blit(level_surface, (x, y))
        
        # Skills (show active skills)
        y += 30
        if player.skills:
            skills_text = f"{get_text('skills')}:"
            skills_surface = self.small_font.render(skills_text, True, WHITE)
            screen.blit(skills_surface, (x, y))
            y += 20
            
            for skill_name, level in list(player.skills.items())[:5]:  # Show max 5 skills
                if skill_name in SKILLS:
                    skill_display = f"{get_skill_name(skill_name)} ({level})"
                    skill_surface = self.small_font.render(skill_display, True, YELLOW)
                    screen.blit(skill_surface, (x, y))
                    y += 18
                    
    def draw_health_bar(self, screen, player, x, y):
        """Draw health bar for player"""
        # Background
        pygame.draw.rect(screen, DARK_GRAY, (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        
        # Health
        if player.max_hp > 0:
            health_width = int((player.hp / player.max_hp) * HEALTH_BAR_WIDTH)
            pygame.draw.rect(screen, RED, (x, y, health_width, HEALTH_BAR_HEIGHT))
            
        # Border
        pygame.draw.rect(screen, WHITE, (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT), 2)
        
        # Text
        health_text = f"{int(player.hp)}/{int(player.max_hp)}"
        text_surface = self.small_font.render(health_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x + HEALTH_BAR_WIDTH // 2, y + HEALTH_BAR_HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        
    def draw_xp_bar(self, screen, player, x, y):
        """Draw XP bar for player"""
        # Background
        pygame.draw.rect(screen, DARK_GRAY, (x, y, XP_BAR_WIDTH, XP_BAR_HEIGHT))
        
        # XP
        if player.xp_to_next_level > 0:
            xp_width = int((player.xp / player.xp_to_next_level) * XP_BAR_WIDTH)
            pygame.draw.rect(screen, BLUE, (x, y, xp_width, XP_BAR_HEIGHT))
            
        # Border
        pygame.draw.rect(screen, WHITE, (x, y, XP_BAR_WIDTH, XP_BAR_HEIGHT), 1)
        
        # Text
        xp_text = f"{player.xp}/{player.xp_to_next_level}"
        text_surface = self.small_font.render(xp_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x + XP_BAR_WIDTH // 2, y + XP_BAR_HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        
    def draw_wave_info(self, screen, current_wave, enemies_remaining=0):
        """Draw current wave information"""
        wave_text = f"{get_text('wave')} {current_wave}"
        wave_surface = self.large_font.render(wave_text, True, WHITE)
        wave_rect = wave_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(wave_surface, wave_rect)
        
        if enemies_remaining > 0:
            enemies_text = f"{get_text('enemies')}: {enemies_remaining}"
            enemies_surface = self.font.render(enemies_text, True, WHITE)
            enemies_rect = enemies_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(enemies_surface, enemies_rect)
            
    def draw_game_over(self, screen, final_wave, final_score=0):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = get_text('game_over').upper()
        game_over_surface = self.large_font.render(game_over_text, True, RED)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(game_over_surface, game_over_rect)
        
        # Final stats
        wave_text = f"{get_text('final_wave')}: {final_wave}"
        wave_surface = self.font.render(wave_text, True, WHITE)
        wave_rect = wave_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(wave_surface, wave_rect)
        
        # Instructions
        restart_text = "Press R to restart or ESC to quit"  # Keep English for key instructions
        restart_surface = self.font.render(restart_text, True, WHITE)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_surface, restart_rect)
        
    def draw_wave_break(self, screen, next_wave, time_remaining):
        """Draw wave break countdown"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Wave complete text
        complete_text = f"{get_text('wave_break')}!"
        complete_surface = self.large_font.render(complete_text, True, GREEN)
        complete_rect = complete_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(complete_surface, complete_rect)
        
        # Next wave countdown
        countdown_text = f"{get_text('next_wave')} {int(time_remaining) + 1}s"
        countdown_surface = self.font.render(countdown_text, True, WHITE)
        countdown_rect = countdown_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(countdown_surface, countdown_rect)
        
        # Next wave number
        next_text = f"{get_text('wave')} {next_wave}"
        next_surface = self.font.render(next_text, True, YELLOW)
        next_rect = next_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(next_surface, next_rect)


class SkillSelectionUI:
    def __init__(self):
        # Try to use a system font that supports Chinese characters
        try:
            self.font = pygame.font.SysFont('simsun,arial,helvetica', UI_FONT_SIZE)
            self.small_font = pygame.font.SysFont('simsun,arial,helvetica', UI_SMALL_FONT_SIZE)
            self.large_font = pygame.font.SysFont('simsun,arial,helvetica', UI_LARGE_FONT_SIZE)
        except:
            # Fallback to default font
            self.font = pygame.font.Font(None, UI_FONT_SIZE)
            self.small_font = pygame.font.Font(None, UI_SMALL_FONT_SIZE)
            self.large_font = pygame.font.Font(None, UI_LARGE_FONT_SIZE)
        
        # Track active skill selections for both players
        self.player1_selection = {'active': False, 'player': None, 'options': []}
        self.player2_selection = {'active': False, 'player': None, 'options': []}
        
    def show(self, player):
        """Show skill selection for a player"""
        # Check if this player already has an active selection
        if player.player_id == 1 and self.player1_selection['active']:
            return  # Already showing selection for this player
        elif player.player_id == 2 and self.player2_selection['active']:
            return  # Already showing selection for this player
            
        # Get available skills
        available_skills = player.get_available_skills()
        
        # Randomly select 3 skills
        if len(available_skills) >= 3:
            skill_options = random.sample(available_skills, 3)
        else:
            skill_options = available_skills[:]
            
        # Assign to appropriate player slot
        if player.player_id == 1:
            self.player1_selection = {'active': True, 'player': player, 'options': skill_options}
        else:
            self.player2_selection = {'active': True, 'player': player, 'options': skill_options}
            
    def hide(self, player_id=None):
        """Hide skill selection for a specific player or all players"""
        if player_id == 1 or player_id is None:
            self.player1_selection = {'active': False, 'player': None, 'options': []}
        if player_id == 2 or player_id is None:
            self.player2_selection = {'active': False, 'player': None, 'options': []}
        
    def handle_input(self, event):
        """Handle input for skill selection using number keys"""
        if event.type == pygame.KEYDOWN:
            # Player 1 keys (left side of keyboard: 1, 2, 3)
            if self.player1_selection['active']:
                if event.key == pygame.K_1:
                    return self._select_skill(1, 0)
                elif event.key == pygame.K_2:
                    return self._select_skill(1, 1)
                elif event.key == pygame.K_3:
                    return self._select_skill(1, 2)
                    
            # Player 2 keys (right side of keyboard: numpad 1, 2, 3 or regular keys if no numpad)
            if self.player2_selection['active']:
                if event.key == pygame.K_KP1 or (event.key == pygame.K_1 and not self.player1_selection['active']):
                    return self._select_skill(2, 0)
                elif event.key == pygame.K_KP2 or (event.key == pygame.K_2 and not self.player1_selection['active']):
                    return self._select_skill(2, 1)
                elif event.key == pygame.K_KP3 or (event.key == pygame.K_3 and not self.player1_selection['active']):
                    return self._select_skill(2, 2)
                    
        return None
        
    def _select_skill(self, player_id, option_index):
        """Select a skill for a player"""
        selection = self.player1_selection if player_id == 1 else self.player2_selection
        
        if selection['active'] and option_index < len(selection['options']):
            selected_skill = selection['options'][option_index]
            return {'player_id': player_id, 'skill': selected_skill}
            
        return None
        
    def draw(self, screen):
        """Draw skill selection UI in side panels"""
        # Draw Player 1 selection (left side)
        if self.player1_selection['active']:
            self._draw_player_selection(screen, self.player1_selection, 'left')
            
        # Draw Player 2 selection (right side)
        if self.player2_selection['active']:
            self._draw_player_selection(screen, self.player2_selection, 'right')
            
    def _draw_player_selection(self, screen, selection, side):
        """Draw skill selection for one player"""
        player = selection['player']
        options = selection['options']
        
        # Panel dimensions
        panel_width = 250
        panel_height = SCREEN_HEIGHT - 100
        
        if side == 'left':
            panel_x = 20
        else:
            panel_x = SCREEN_WIDTH - panel_width - 20
            
        panel_y = 50
        
        # Semi-transparent panel background
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(200)
        panel_surface.fill(DARK_GRAY)
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Panel border
        pygame.draw.rect(screen, YELLOW, (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Title
        title_text = f"Player {player.player_id} - Level {player.level}!"
        title_surface = self.font.render(title_text, True, YELLOW)
        title_rect = title_surface.get_rect(centerx=panel_x + panel_width // 2, y=panel_y + 10)
        screen.blit(title_surface, title_rect)
        
        # Choose skill text
        choose_text = "Choose Skill:"
        choose_surface = self.small_font.render(choose_text, True, WHITE)
        choose_rect = choose_surface.get_rect(centerx=panel_x + panel_width // 2, y=panel_y + 40)
        screen.blit(choose_surface, choose_rect)
        
        # Skill options
        option_height = 80
        option_spacing = 10
        start_y = panel_y + 80
        
        for i, skill_name in enumerate(options):
            if skill_name in SKILLS:
                skill_data = SKILLS[skill_name]
                
                # Option background
                option_rect = pygame.Rect(
                    panel_x + 10,
                    start_y + i * (option_height + option_spacing),
                    panel_width - 20,
                    option_height
                )
                
                # Option background color
                pygame.draw.rect(screen, GRAY, option_rect)
                pygame.draw.rect(screen, WHITE, option_rect, 2)
                
                # Key number indicator
                key_text = f"{i + 1}"
                key_surface = self.large_font.render(key_text, True, YELLOW)
                key_rect = key_surface.get_rect(x=option_rect.x + 5, y=option_rect.y + 5)
                screen.blit(key_surface, key_rect)
                
                # Skill name
                name_surface = self.small_font.render(get_skill_name(skill_name), True, WHITE)
                name_rect = name_surface.get_rect(
                    x=option_rect.x + 30,
                    y=option_rect.y + 5
                )
                screen.blit(name_surface, name_rect)
                
                # Skill description
                desc_surface = self.small_font.render(get_skill_description(skill_name), True, LIGHT_GRAY)
                desc_rect = desc_surface.get_rect(
                    x=option_rect.x + 5,
                    y=option_rect.y + 25
                )
                screen.blit(desc_surface, desc_rect)
                
                # Current level if applicable
                current_level = player.skills.get(skill_name, 0)
                max_level = skill_data['max_level']
                if current_level > 0:
                    level_info = f"Lv{current_level}→{current_level + 1} (Max:{max_level})"
                else:
                    level_info = f"New (Max:{max_level})"
                    
                level_surface = self.small_font.render(level_info, True, YELLOW)
                level_rect = level_surface.get_rect(
                    x=option_rect.x + 5,
                    y=option_rect.y + 50
                )
                screen.blit(level_surface, level_rect)
                
        # Instructions at bottom
        if side == 'left':
            instruction_text = "Press 1, 2, or 3"
        else:
            instruction_text = "Press Numpad 1, 2, or 3"
            
        instruction_surface = self.small_font.render(instruction_text, True, WHITE)
        instruction_rect = instruction_surface.get_rect(
            centerx=panel_x + panel_width // 2,
            y=panel_y + panel_height - 30
        )
        screen.blit(instruction_surface, instruction_rect)


class MainMenu:
    def __init__(self):
        # Try to use a system font that supports Chinese characters
        try:
            self.font = pygame.font.SysFont('simsun,arial,helvetica', UI_FONT_SIZE)
            self.large_font = pygame.font.SysFont('simsun,arial,helvetica', UI_LARGE_FONT_SIZE)
            self.title_font = pygame.font.SysFont('simsun,arial,helvetica', 72)
        except:
            # Fallback to default font
            self.font = pygame.font.Font(None, UI_FONT_SIZE)
            self.large_font = pygame.font.Font(None, UI_LARGE_FONT_SIZE)
            self.title_font = pygame.font.Font(None, 72)
        
    def draw(self, screen):
        """Draw main menu"""
        screen.fill(BLACK)
        
        # Title
        title_text = "DUAL FURY"
        title_surface = self.title_font.render(title_text, True, YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "Cooperative Survival Game"  # Keep English for game subtitle
        subtitle_surface = self.large_font.render(subtitle_text, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Instructions
        instructions = [
            "Player 1: WASD to move, Q to attack/shoot",  # Updated controls
            "Player 2: Arrow keys to move, K to attack/shoot",
            "",
            "Short press Q/K: Melee attack or quick shot",
            "Long press Q/K: Special weapon (when unlocked)",
            "Unlock 'Ranged Combat' skill to enable shooting!",
            "",
            get_text('press_space'),
            get_text('press_q')
        ]
        
        start_y = 350
        for i, instruction in enumerate(instructions):
            if instruction:  # Skip empty lines
                color = YELLOW if "Press" in instruction else WHITE
                instruction_surface = self.font.render(instruction, True, color)
                instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 30))
                screen.blit(instruction_surface, instruction_rect)
            else:
                start_y += 10  # Add extra space for empty lines
                
    def handle_input(self, event):
        """Handle main menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return 'start_game'
            elif event.key == pygame.K_ESCAPE:
                return 'quit'
        return None