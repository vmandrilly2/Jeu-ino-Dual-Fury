import pygame
import random
from settings import *

class UI:
    def __init__(self):
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
        label = f"Player {player.player_id}"
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
        level_text = f"Level: {player.level}"
        level_surface = self.font.render(level_text, True, WHITE)
        screen.blit(level_surface, (x, y))
        
        # Skills (show active skills)
        y += 30
        if player.skills:
            skills_text = "Skills:"
            skills_surface = self.small_font.render(skills_text, True, WHITE)
            screen.blit(skills_surface, (x, y))
            y += 20
            
            for skill_name, level in list(player.skills.items())[:5]:  # Show max 5 skills
                if skill_name in SKILLS:
                    skill_display = f"{SKILLS[skill_name]['name']} ({level})"
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
        wave_text = f"Wave {current_wave}"
        wave_surface = self.large_font.render(wave_text, True, WHITE)
        wave_rect = wave_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(wave_surface, wave_rect)
        
        if enemies_remaining > 0:
            enemies_text = f"Enemies: {enemies_remaining}"
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
        game_over_text = "GAME OVER"
        game_over_surface = self.large_font.render(game_over_text, True, RED)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(game_over_surface, game_over_rect)
        
        # Final stats
        wave_text = f"Final Wave: {final_wave}"
        wave_surface = self.font.render(wave_text, True, WHITE)
        wave_rect = wave_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(wave_surface, wave_rect)
        
        # Instructions
        restart_text = "Press R to restart or ESC to quit"
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
        complete_text = "Wave Complete!"
        complete_surface = self.large_font.render(complete_text, True, GREEN)
        complete_rect = complete_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(complete_surface, complete_rect)
        
        # Next wave countdown
        countdown_text = f"Next wave in {int(time_remaining) + 1} seconds"
        countdown_surface = self.font.render(countdown_text, True, WHITE)
        countdown_rect = countdown_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(countdown_surface, countdown_rect)
        
        # Next wave number
        next_text = f"Wave {next_wave}"
        next_surface = self.font.render(next_text, True, YELLOW)
        next_rect = next_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(next_surface, next_rect)


class SkillSelectionUI:
    def __init__(self):
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.small_font = pygame.font.Font(None, UI_SMALL_FONT_SIZE)
        self.large_font = pygame.font.Font(None, UI_LARGE_FONT_SIZE)
        
        self.active = False
        self.player = None
        self.skill_options = []
        self.selected_option = 0
        
    def show(self, player):
        """Show skill selection for a player"""
        self.active = True
        self.player = player
        self.selected_option = 0
        
        # Get available skills
        available_skills = player.get_available_skills()
        
        # Randomly select 3 skills
        if len(available_skills) >= 3:
            self.skill_options = random.sample(available_skills, 3)
        else:
            self.skill_options = available_skills[:]
            
    def hide(self):
        """Hide skill selection"""
        self.active = False
        self.player = None
        self.skill_options = []
        
    def handle_input(self, event):
        """Handle input for skill selection"""
        if not self.active:
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.skill_options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.skill_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.skill_options:
                    selected_skill = self.skill_options[self.selected_option]
                    return selected_skill
                    
        return None
        
    def draw(self, screen):
        """Draw skill selection UI"""
        if not self.active or not self.player:
            return
            
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(SKILL_SELECTION_BACKGROUND_ALPHA)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Title
        title_text = f"Player {self.player.player_id} - Choose a Skill"
        title_surface = self.large_font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)
        
        # Level up text
        level_text = f"Level {self.player.level}!"
        level_surface = self.font.render(level_text, True, YELLOW)
        level_rect = level_surface.get_rect(center=(SCREEN_WIDTH // 2, 180))
        screen.blit(level_surface, level_rect)
        
        # Skill options
        start_y = 250
        for i, skill_name in enumerate(self.skill_options):
            if skill_name in SKILLS:
                skill_data = SKILLS[skill_name]
                
                # Option background
                option_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - SKILL_OPTION_WIDTH // 2,
                    start_y + i * (SKILL_OPTION_HEIGHT + SKILL_OPTION_SPACING),
                    SKILL_OPTION_WIDTH,
                    SKILL_OPTION_HEIGHT
                )
                
                # Highlight selected option
                if i == self.selected_option:
                    pygame.draw.rect(screen, YELLOW, option_rect, 3)
                    pygame.draw.rect(screen, DARK_GRAY, option_rect)
                else:
                    pygame.draw.rect(screen, GRAY, option_rect)
                    
                pygame.draw.rect(screen, WHITE, option_rect, 2)
                
                # Skill name
                name_surface = self.font.render(skill_data['name'], True, WHITE)
                name_rect = name_surface.get_rect(
                    centerx=option_rect.centerx,
                    y=option_rect.y + 10
                )
                screen.blit(name_surface, name_rect)
                
                # Skill description
                desc_surface = self.small_font.render(skill_data['description'], True, LIGHT_GRAY)
                desc_rect = desc_surface.get_rect(
                    centerx=option_rect.centerx,
                    y=option_rect.y + 35
                )
                screen.blit(desc_surface, desc_rect)
                
                # Current level if applicable
                current_level = self.player.skills.get(skill_name, 0)
                max_level = skill_data['max_level']
                if current_level > 0:
                    level_info = f"Level {current_level} → {current_level + 1} (Max: {max_level})"
                else:
                    level_info = f"New skill (Max: {max_level})"
                    
                level_surface = self.small_font.render(level_info, True, YELLOW)
                level_rect = level_surface.get_rect(
                    centerx=option_rect.centerx,
                    y=option_rect.y + 60
                )
                screen.blit(level_surface, level_rect)
                
        # Instructions
        instruction_text = "Use W/S or ↑/↓ to select, ENTER or SPACE to choose"
        instruction_surface = self.small_font.render(instruction_text, True, WHITE)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instruction_surface, instruction_rect)


class MainMenu:
    def __init__(self):
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
        subtitle_text = "Cooperative Survival Game"
        subtitle_surface = self.large_font.render(subtitle_text, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Instructions
        instructions = [
            "Player 1: WASD to move, Q to attack",
            "Player 2: Arrow keys to move, K to attack",
            "",
            "Survive waves of enemies and level up!",
            "",
            "Press SPACE to start",
            "Press ESC to quit"
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