import time
import pypresence

CLIENT_ID = 688089938985615401

class DiscordRPCIntegration:

    def __init__(self, main):
        self.main = main
        self.presence = pypresence.Presence(CLIENT_ID)

        self.main.logger.info('DISCORD_RPC_INTEGRATION INITIALISED')

    def update_for_startScreen(self):
        if self.main.settings['discord_rpc']:
            try:
                mainMenu_name = self.main.lang_manager.get_string('Other', 'MainMenu')

                self.presence.update(details=mainMenu_name,
                                     large_image='sheymosu_logo',
                                     start=time.time())

            except Exception as e:
                self.main.logger.error('DISCORD PRESENCE UPDATING IS FAILED: %s', e)

    def update_for_gameplayScreen(self):
        if self.main.settings['discord_rpc']:
            try:
                gamemode_name = self.main.lang_manager.get_string_by_code('GameMode', self.main.current_save['gamemode'])
                gamemode_name = self.main.lang_manager.get_string('GameMode', gamemode_name)

                difficulty_name = self.main.lang_manager.get_string_by_code('Difficulty', self.main.current_save['difficulty'])
                difficulty_name = self.main.lang_manager.get_string('Difficulty', difficulty_name)

                self.presence.update(details=gamemode_name,
                                     state=difficulty_name,
                                     large_image='sheymosu_logo',
                                     start=time.time())

            except Exception as e:
                self.main.logger.error('DISCORD PRESENCE UPDATING IS FAILED: %s', e)
