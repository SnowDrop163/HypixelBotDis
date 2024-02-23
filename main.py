import discord
from discord.ext import commands, tasks
from discord.ui import Button, View, Modal, TextInput
from discord import app_commands
import requests
from config import settings, roles, channels
import youtube_dl
from async_timeout import timeout
import asyncio
import functools
import itertools
import math
import random

youtube_dl.utils.bug_reports_message = lambda: '' #Удаление не нужных ошибок


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass



BOT_TOKEN = settings['token']
HYPIXEL_API_KEY = settings['hypixels_apis']
GUILD_ID = settings['id_server']

VERIFIED_ROLE_ID = roles['verificated']
ADMIN_ROLE_ID = roles['admins']
MUSIC_ROLE_ID = roles['music']

NEWS_CHANNEL_ID = channels['news']
ADMIN_CHANNEL_ID = channels['admin']
VERIFY_CHANEL_ID = channels['verify']
GUILD_INFO_CHANEL_ID = channels['info']
TERMS_CHANEL_ID = channels['terms']
MASTERMODE_CHANNEL_ID = channels['master']
DUNGEON_CHANNEL_ID = channels['dungeon']
RULES_CHANNEL_ID = channels['rules']
SLAYER_CHANNEL_ID = channels['slayer']
KUUDRA_CHANNEL_ID = channels['kuudra']
BREWING_CHANNEL_ID = channels['brewing']

HYPIXEL_RANKS_TO_DISCORD_ROLE_IDS = {
    "VIP": roles['vip'],
    "VIP+": roles['vip+'],
    "MVP": roles['mvp'],
    "MVP+": roles['mvp+'],
    "MVP++": roles['mvp++']
}

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)



def get_hypixel_player_data(nickname):
    hypixel_api_url = f'https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&name={nickname}'
    response = requests.get(hypixel_api_url)

    return response.json() if response.ok else None

def convert_rank(api_rank):
    rank_conversion = {
        "VIP_PLUS": "VIP+",
        "MVP_PLUS": "MVP+",
        "MVP_PLUS_PLUS": "MVP++"
    }

    return rank_conversion.get(api_rank, api_rank)


class StartVerificationView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=None)
    @discord.ui.button(label="Верификация✅", style=discord.ButtonStyle.green, custom_id="start_verification")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Прежде чем начать, внимательно ознакомьтесь",
                              description="- Мы **единственный** и офицальный Marvelous Elite Forces Discord, и единственная ссылка для приглашения — https://discord.gg/Rmrh3vppFA. Любые другие Discord каналы с именем `MEF` **пытаются украсть ваш аккаунт**!!!\n- Ни один Minecraft Discord не спросит у вас адрес электронной почты. Никогда не вводите **свои личные данные или пароли** ботам в Discord.\n-  <@1196539600294916136> — **единственные** настоящий бот Marvelous Elite Forces.\n\n Запомните данную информацию.",
                              color=discord.Color.gold())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, view=AcceptDeclineView(), ephemeral=True)

    @discord.ui.button(label="Выдача роли привелегии👑", style=discord.ButtonStyle.red, custom_id="assign_rank_role")
    async def rank_role_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Привелегии Hypixel и их преимущества в дискорд канале",
                              description="**Привелегии**:\n\n <:vip:1201256482671448186> **VIP** \n- Дает доступ к **приватному чату** и **голосовому каналу** \n\n <:vip_plus:1201256181704966295> **VIP+** \n- Дает доступ к **приватному чату** и **голосовому каналу** (включая чаты и голосовые каналы доступные **VIP**)\n\n <:mvp:1201256179209351168> **MVP** \n- Дает доступ к **приватному чату** и **голосовому каналу** (включая чаты и голосовые каналы доступные **VIP** и **VIP+**)\n\n <:mvp_plus:1201256177078632478> **MVP+** \n- Дает доступ к **приватному чату** и **голосовому каналу** (включая чаты и голосовые каналы доступные **VIP**, **VIP+** и **MVP**)\n\n<:mvp_plus_plus:1201256173593174076> **MVP++** \n- Дает доступ к **приватному чату** и **голосовому каналу**, а также дает **2%** скидку на все услуги от гильдии (включая чаты и голосовые каналы доступные **VIP**, **VIP+**, **MVP** и **MVP+**)",
                              color=discord.Color.red())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, view=RequestRoleView(), ephemeral=True)


class InformationView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=None)
    @discord.ui.button(label="Роли", style=discord.ButtonStyle.gray, custom_id="role")
    async def role_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Роли персонала",
                              description="<@&1197859705033326633> – команда лидеров Marvelous Elite Forces, обеспечивающая работу сервера\n<@&1203739269206773890> — старшие модераторы с дополнительными правами\n<@&1203739272402964592> — модераторы чата, отвечают на тикеты в службе поддержки и помогают участникам\n<@&1203739276349546586> — стажеры, которые были приняты на испытательный срок\n<@&1203739288064237699> — весь состав имеет такую роль, не стесняйтесь обращаться к нам в любое время, создав тикет в канале <#1201205857011105863>",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        embed1 = discord.Embed(
            title="Carrier Roles",
            description="**Dungeon Carrier**\n<@&1206952885146091560> _ _ Люди с этой ролью керрят вам 7-ые этажи в катакомбах\n<@&1206952889482747925> _ _  Люди с этой ролью керрят вам 6-ые этажи в катакомбах\n<@&1206952894755250256> _ _  Люди с этой ролью керрят вам 5-ые этажи в катакомбах\n<@&1206952930859687956> _ _  Люди с этой ролью керрят вам 4-и этажи в катакомбах\n**Master Mode Carrier**\n<@&1206953847134748672> _ _  Люди с этой ролью керрят вам 7-ые этажи в катакомбах (Мастер Мод)\n<@&1206953850829934613> _ _  Люди с этой ролью керрят вам 6-ые этажи в катакомбах (Мастер Мод)\n<@&1206953853812215859> _ _  Люди с этой ролью керрят вам 5-ые этажи в катакомбах (Мастер Мод)\n<@&1206953857641488435> _ _  Люди с этой ролью керрят вам 4-ые этажи в катакомбах (Мастер Мод)\n<@&1206953862314074152> _ _  Люди с этой ролью керрят вам 3-и этажи в катакомбах (Мастер Мод)\n<@&1206953865967050803> _ _  Люди с этой ролью керрят вам 2-ые этажи в катакомбах (Мастер Мод)\n<@&1206953869997768714> _ _  Люди с этой ролью керрят вам 1-ые этажи в катакомбах (Мастер Мод)\n**Brewer**\n<@&1206952516642803773> _ _ Люди с этой ролью могут варить вам зелья\n**Slayer Carrier**\n<@&1206962450377740369> _ _ Люди с этой ролью керрят вам уровень 4-ый блейзов\n<@&1206962594062147614> _ _ Люди с этой ролью керрят вам уровень 3-й блейзов\n<@&1206962596952014859> _ _ Люди с этой ролью керрят вам уровень 2-ой блейзов\n<@&1206957311185256549> _ _ Люди с этой ролью керрят вам уровень 4-ый эндерменов\n<@&1206957314872057946> _ _ Люди с этой ролью керрят вам уровень 3-й эндерменов\n<@&1207323947268444170> _ _ Люди с этой ролью керрят вам уровень 5-ый ревенанта\n**Kuudra Carrier**\n<@&1206959676495761438> _ _ Люди с этой ролью керрят вам уровень Infernal куудру\n<@&1206959679285108756> _ _ Люди с этой ролью керрят вам уровень Fiery куудру\n<@&1206959257506021396> _ _ Люди с этой ролью керрят вам уровень Burning куудру\n<@&1206959267652042822> _ _ Люди с этой ролью керрят вам уровень Hot куудру\n<@&1206957305414025266> _ _ Люди с этой ролью керрят вам уровень Basic куудру\n**Наказания**\n<@&1205079746057084958> _ _ Выдаются, за 5 варнов, людям, которые заказывают керри и при этом нарушают словия предоставления услуг\n<@&1207626797466783754> _ _ Выдаются людям, которые предостовляют любые наши услуги при нарушении правил и/или получении 3-ёх страйков",
            color=discord.Color.green()
        )
        embed1.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed1.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.send_message(embed=embed1, ephemeral=True)

    @discord.ui.button(label="ЧаВо", style=discord.ButtonStyle.gray, custom_id="faq")
    async def faq_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="",
                              description="",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Как оставаться в безопасности", style=discord.ButtonStyle.gray, custom_id="safe")
    async def safe_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="",
                              description="",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Наша гильдия", style=discord.ButtonStyle.gray, custom_id="guilds")
    async def guilds_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="",
                              description="",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class MasterModeView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=None)

    @discord.ui.button(label="Master Mode 1", style=discord.ButtonStyle.red, custom_id="mm1",  emoji="<:bonzo:1205283252487716924>")
    async def master1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Inactive for you",
                              description="Go nahuy",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Master Mode 2", style=discord.ButtonStyle.red, custom_id="mm2",  emoji="<:scarf:1205283251003072543>")
    async def master2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Inactive for you",
                              description="Go nahuy",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Master Mode 3", style=discord.ButtonStyle.red, custom_id="mm3",  emoji="<:professor:1205283249572675594>")
    async def master3(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Inactive for you",
                              description="Go nahuy",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Master Mode 4", style=discord.ButtonStyle.red, custom_id="mm4",  emoji="<:Thorn:1205283247903211730>")
    async def master4(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Inactive for you",
                              description="Go nahuy",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Master Mode 5", style=discord.ButtonStyle.red, custom_id="mm5",  emoji="<:livid:1205283246099660810>")
    async def master5(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Inactive for you",
                              description="Go nahuy",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Master Mode 6", style=discord.ButtonStyle.red, custom_id="mm6", emoji="<:sadan:1205283244312895488>")
    async def master6(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Inactive for you",
                              description="Go nahuy",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Master Mode 7", style=discord.ButtonStyle.red, custom_id="mm7", emoji="<:necron:1205283242698219540>")
    async def master7(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Inactive for you",
                              description="Go nahuy",
                              color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class AcceptDeclineView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=None)

    @discord.ui.button(label="Продолжить", style=discord.ButtonStyle.green, custom_id="accept_verification")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        embed = discord.Embed(title="Верификация", description=f"Чтобы верифицировать аккаунт, обязательно выполнить следующие действия:\n- Войдите в Hypixel\n- Возьмите из инвентаря в руку голову вашего игрока и нажмите ПКМ\n- Нажмите ЛКМ по `Социальные сети`, а затем ЛКМ по `Discord`\n- Откройте чат, вставьте `{str(interaction.user)}` и нажмите Enter\n- Теперь вы можете нажать на кнопку ниже и ввести свой **Minecraft ник**, чтобы закончить верификацию\n\n Краткий туториал на гифке:",
                              color=discord.Color.blue())
        embed.set_image(url="https://i.postimg.cc/Qtfq7hVQ/verify-6.gif")
        embed.set_thumbnail(
            url="https://i.postimg.cc/9FH3tx4X/standard.gif")
        embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")

        await interaction.response.edit_message(embed=embed, view=EnterNickView())

class RequestRoleView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=None)
    @discord.ui.button(label="Ввести ник", style=discord.ButtonStyle.green, custom_id="enter_nickname_for_rank")
    async def enter_nick_for_rank_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(NicknameForRoleModal())
        except Exception as e:
            print(f"Произошла ошибка: {e}")

class EnterNickView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=None)
    @discord.ui.button(label="Ввести ник", style=discord.ButtonStyle.green, custom_id="enter_nickname")
    async def enter_nick_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(NicknameModal())
        except Exception as e:
            print(f"Произошла ошибка: {e}")


class NicknameModal(Modal):
    def __init__(self):
        super().__init__(title="Введите ваш никнейм из Hypixel")
        self.nickname = TextInput(
            label="Никнейм",
            style=discord.TextStyle.short,
            placeholder='Ваш ник в Minecraft',
            min_length=3,
            max_length=32
        )
        self.add_item(self.nickname)

    async def on_submit(self, interaction: discord.Interaction):
        player_data = get_hypixel_player_data(self.nickname.value)
        if not player_data or not player_data.get('success'):
            await interaction.response.send_message(embed=discord.Embed(
                title="Ошибка",
                description="Ошибка связи с API Hypixel.",
                color=discord.Color.red()), ephemeral=True)
            return

        if not player_data or not player_data.get('player'):
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Ошибка",
                    description="Пользователь не найден на сервере Hypixel.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

        discord_id = str(interaction.user)
        if player_data['player'].get('socialMedia', {}).get('links', {}).get('DISCORD') != discord_id:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Ошибка",
                    description="Ваш Discord не совпадает с тем, что связан с учетной записью Hypixel.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

        try:
            await interaction.user.edit(nick=self.nickname.value)
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Ошибка",
                    description="У меня нет прав изменить Ваш ник.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

        guild = interaction.guild
        role = guild.get_role(VERIFIED_ROLE_ID)
        if role:
            try:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Верификация прошла успешно!",
                        description=f"Ваш ник изменён на {self.nickname.value} и вы получили верифицированную роль.",
                        color=discord.Color.green()
                    ),
                    ephemeral=True
                )
            except discord.Forbidden:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Ошибка",
                        description="У меня нет прав выдать Вам роль.",
                        color=discord.Color.red()
                    ),
                    ephemeral=True
                )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Ошибка",
                    description="Не удалось найти роль для верификации.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )

class NicknameForRoleModal(Modal):
    def __init__(self):
        super().__init__(title="Введите ваш никнейм из Hypixel")
        self.nickname = TextInput(
            label="Никнейм",
            style=discord.TextStyle.short,
            placeholder='Ваш ник в Minecraft',
            min_length=3,
            max_length=32
        )
        self.add_item(self.nickname)

    async def on_submit(self, interaction: discord.Interaction):
        player_data = get_hypixel_player_data(self.nickname.value)
        if not player_data or not player_data.get('success'):
            await interaction.response.send_message(embed=discord.Embed(
                title="Ошибка",
                description="Ошибка связи с API Hypixel.",
                color=discord.Color.red()), ephemeral=True)
            return

        if not player_data.get('player'):
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Ошибка",
                    description="Пользователь не найден на сервере Hypixel.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

        discord_id = str(interaction.user)
        if player_data['player'].get('socialMedia', {}).get('links', {}).get('DISCORD') != discord_id:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Ошибка",
                    description="Ваш Discord не совпадает с тем, что связан с учетной записью Hypixel.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

        api_rank = player_data['player'].get('newPackageRank', player_data['player'].get('packageRank', None))
        if api_rank is None:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Ошибка",
                    description="Ошибка при получении ранга с сервера Hypixel.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

        api_rank = convert_rank(api_rank)
        discord_role_id = HYPIXEL_RANKS_TO_DISCORD_ROLE_IDS.get(api_rank)

        if discord_role_id:
            discord_role = interaction.guild.get_role(discord_role_id)
            if discord_role:
                try:
                    await interaction.user.add_roles(discord_role)
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="Роль привилегии выдана",
                            description=f"Вам была выдана роль {discord_role.name}",
                            color=discord.Color.green()
                        ),
                        ephemeral=True
                    )
                except discord.Forbidden:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="Ошибка",
                            description="У меня нет прав выдать вам роль.",
                            color=discord.Color.red()
                        ),
                        ephemeral=True
                    )
            else:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Ошибка",
                        description="Роль на сервере не найдена.",
                        color=discord.Color.red()
                    ),
                    ephemeral=True
                )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Ошибка",
                    description="Не удалось найти роль для данного ранга Hypixel.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )


@bot.hybrid_command(name="status", description="Проверка состояния бота")
async def status(interection: discord.Interaction):
    embed = discord.Embed(title="Статус бота", description="Текущий статус бота", color=0x00ff00)
    embed.add_field(name="В сети", value="Да", inline=False)
    embed.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")
    await interection.send(embed=embed)

class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed
class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                try:
                    async with timeout(180):
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music():
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))
    @bot.hybrid_command(name="join", description="Присоединиться в голосовой канал", invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @bot.hybrid_command(name="summon", description="Присоединиться в голосовой канал")
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):


        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()


    @bot.hybrid_command(name="leave", description="Очищает очередь и покидает голосовой канал")
    async def _leave(self, ctx: commands.Context):


        if not ctx.voice_state.voice:
            return await ctx.send('Не подключен к войсу')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @bot.hybrid_command(name="volume", description="Устанавливает громкость")
    @app_commands.describe(volume="Напишите значение от 0 до 100")
    async def _volume(self, ctx: commands.Context, *, volume: int):

        if not ctx.voice_state.is_playing:
            return await ctx.send('В данный момент ничего не играет')

        if 0 > volume > 100:
            return await ctx.send('Укажите значения от 0 до 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Громкость плеера установлена на {}%'.format(volume))

    @bot.hybrid_command(name="now", description="Отображает воспроизводимую в данный момент песню")
    async def _now(self, ctx: commands.Context):

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @bot.hybrid_command(name="pause", description="Ставит текущий трек на паузу")
    async def _pause(self, ctx: commands.Context):


        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @bot.hybrid_command(name="resume", description="Продолжает воспроизведение трека")
    async def _resume(self, ctx: commands.Context):


        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @bot.hybrid_command(name="stop", description="Полностью останавливает проигрывание песни и очищает очередь")
    async def _stop(self, ctx: commands.Context):

        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @bot.hybrid_command(name="skip", description="Пропускает песню, если 3 человека проголосовали за ее пропуск")
    async def _skip(self, ctx: commands.Context):

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    @bot.hybrid_command(name="queue", description="Показывает лист ожидания очереди")
    @app_commands.describe(page="Укажите номер страницы")
    async def _queue(self, ctx: commands.Context, *, page: int = 1):

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="shuffle", description="Перемешивает треки в листе ожидания")
    async def _shuffle(self, ctx: commands.Context):

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Очередь пуста")

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @bot.hybrid_command(name="remove", description="Удаляет песню из очереди по заданному индексу.")
    @app_commands.describe(index="Номер песни")
    async def _remove(self, ctx: commands.Context, index: int):

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Очередь пуста")

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @bot.hybrid_command(name="loop", description="Зацикливает играющий в данный момент трек")
    async def _loop(self, ctx: commands.Context):

        if not ctx.voice_state.is_playing:
            return await ctx.send("В данный момент ничего не играет.")

        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @bot.hybrid_command(name="play", description="Введите название трека или ссылку из ютуба на него")
    @app_commands.describe(search="Найдется все")
    async def _play(self, ctx: commands.Context, *, search: str):

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send("При обработке этого запроса произошла ошибка: {}".format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send("В очереди {}".format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("Вы не подключены  войсу")

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Бот находится в другом войс канале')


async def embedinf():

    channel = bot.get_channel(VERIFY_CHANEL_ID)
    channel1 = bot.get_channel(ADMIN_CHANNEL_ID)
    channel2 = bot.get_channel(GUILD_INFO_CHANEL_ID)
    channel3 = bot.get_channel(TERMS_CHANEL_ID)
    channel4 = bot.get_channel(MASTERMODE_CHANNEL_ID)
    channel5 = bot.get_channel(DUNGEON_CHANNEL_ID)
    channel6 = bot.get_channel(RULES_CHANNEL_ID)
    channel7 = bot.get_channel(SLAYER_CHANNEL_ID)
    channel8 = bot.get_channel(KUUDRA_CHANNEL_ID)
    channel9 = bot.get_channel(BREWING_CHANNEL_ID)

    await channel.purge(limit=100)
    await channel1.purge(limit=100)
    await channel2.purge(limit=100)
    await channel3.purge(limit=100)
    await channel4.purge(limit=100)
    await channel5.purge(limit=100)
    await channel6.purge(limit=100)
    await channel7.purge(limit=100)
    await channel8.purge(limit=100)
    await channel9.purge(limit=100)

    embed1 = discord.Embed(
    title="Статус бота",
    description=f"{bot.user} возобновил работу!",

    color=discord.Color.green()
    )
    embed1.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed1.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")

    embed2 = discord.Embed(
        title="Добро пожаловать в Marvelous Elite Forces",
        description="Мы — дружелюбное сообщество с небольшим количеством игроков — новички, эксперты и даже рекордсмены мира!\n\nЕсли хотите узнать о нас по подробнее **нажмите одну из кнопок ниже**.\nЧтобы получить полный доступ к серверу, включая каналы керри, пожалуйста верифецируйте свой аккаунт в канале <#1196455861472722984>.",

        color=discord.Color.green()
    )
    embed2.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed2.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")

    embed3 = discord.Embed(
        title="Условия предоставления услуг Marvelous Elite Forces",
        description="Эти условия были разработаны, чтобы обеспечить наилучшие результаты как для нашей сервисной команды, так и для наших клиентов.\n\n- Убедитесь, что никнейм в Discord вашего оператора связи и ник в Minecraft совпадают. Мы не несем ответственности, если вас обманули из-за несоблюдения этого правила.\n\n- Вы **обязаны** внести предоплату за все наши услуги, если правило не предусматривает иное.\n\n- При покупке Dungeon Carry (включая режим Master) цена превышает 20 миллионов монет, вы должны платить с шагом 20 миллионов монет. Уточняю, **не платите сразу больше 20м**. Если ваш оператор связи отказывается принимать 20 миллионов монет и просит полную оплату, не стесняйтесь пингануть <@&1205068967438188574> или <@&1203739288064237699>, объяснив это.\n\n- При покупке керри Slayer, цена которого превышает 25 миллионов монет, вы должны заплатить с шагом 25 миллионов монет. Уточняю, **не платите сразу больше 25м**. Если ваш оператор связи отказывается принимать 25 миллионов монет и просит полную оплату, не стесняйтесь пингануть либо  <@&1205068967438188574> или <@&1203739288064237699>, объяснив это.\n\n- Вы не должны проявлять неуважение к нашей сервисной команде. Если член сервисной команды, заявивший о вашей заявке, проявляет неуважение, откройте тикет в <#1201205857011105863> и объясните ситуацию персоналу Discord, вы должны быть готовы предоставить доказательства.\n\n- В <#1204764848592785499> нельзя оставлять ложные отзывы.\n\n- Вы не должны пытаться выполнить массовый пинг. Невыполнение обязательства приведет к отключению звука и, возможно, к <@&1205079746057084958>.\n\n- Все покупки должны совершаться с использованием монет, если только член Service Team, принявший ваш тикет, не возражает.\n\n- Вы должны быть готовы получить выбранную вами услугу при создании тикета.\n\n- Одновременно можно открыть только 1 тикет\n\n- Запрещенно создавать тикеты по просьбе друзей или просить друзей создать вам тикет.\n\nСоздание тикета означает, что вы готовы соблюдать все вышеперечисленные правила.",

        color=discord.Color.green()
    )
    embed3.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed3.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")

    embed4 = discord.Embed(
        title="Условия предоставления услуг",
        description="**1)** Не создавайте тикет на керри, если вы не готовы получить услугу.\n**2)** Оплата производится авансом без исключений.\n**3)** Если вы умрете более 2 раз и приведете к снижению счета по сравнению с тем, который вы заказали, мы не обязаны компенсировать вашу потерю.\n**4)** Если вы отключитесь во время керри на Мастер-режиме Этаж 7 Фаза 5, вам будет возвращена только половина уплаченной суммы, в противном случае вы получите возврат средств за все остальные этажи.\n**5)** Как только вы войдете в Катакомбы, выбранный вами класс будет зависеть от принявшего ваш тикет человека, чтобы керри было более эффективное.\n**6)** Ваш керри считается оконченным, когда вы наберете заказанное количество прохождения того или иного этажа.\n**7)** Весь лут, который вы получите, полностью ваш.\n**8)** Указанные цены не подлежат обсуждению, попытка занизить цену приведет к варну.\n**9)** Не пингуйте членов сервисной команды в вашем тикете, терпеливо ждите, пока кто-нибудь не заберет ваш тикет.\n**10)** Вам не разрешается приглашать других людей на керри. Когда вы платите за керри, вы платите за себя, а не за себя и того, кого вы хотите пригласить. Однако вы можете пригласить других людей, если вы также заплатите за каждого дополнительного человека в партии.\n\n __**Примечания**__ \n\n-  Вам будет выдан варн за нарушение любого из вышеперечисленных правил.\n- Если у вас будет 5 варнов, вы получите черный список тикетов и не сможете открыть ни одного тикета.",

        color=discord.Color.green()
    )
    embed4.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed4.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")

    embed5 = discord.Embed(
        title="<:bonzo:1205283252487716924>Master Mode 1",
        description="**S Runs**\n- 1 run: **1.2m** per\n- 5 or more Runs: **1m** per",

        color=discord.Color.green()
    )
    embed5.set_thumbnail(
        url="https://i.postimg.cc/tC0L3q0J/bonzo.webp")
    embed5.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed6 = discord.Embed(
        title="<:scarf:1205283251003072543>Master Mode 2",
        description="**S Runs**\n- 1 run: **2.3m** per\n- 5 or more Runs: **2.1m** per",

        color=discord.Color.green()
    )
    embed6.set_thumbnail(
        url="https://i.postimg.cc/W3hQntbF/scarf.webp")
    embed6.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed7 = discord.Embed(
        title="<:professor:1205283249572675594>Master Mode 3",
        description="**S Runs**\n- 1 run: **3.5m** per\n- 5 or more Runs: **3.3m** per",

        color=discord.Color.green()
    )
    embed7.set_thumbnail(
        url="https://i.postimg.cc/QCvYSqYv/professor.webp")
    embed7.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed8 = discord.Embed(
        title="<:Thorn:1205283247903211730>Master Mode 4",
        description="**S Runs**\n- 1 run: **15m** per",

        color=discord.Color.green()
    )
    embed8.set_thumbnail(
        url="https://i.postimg.cc/WzdfMy8M/Thorn.webp")
    embed8.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed9 = discord.Embed(
        title="<:livid:1205283246099660810>Master Mode 5",
        description="**S Runs**\n- 1 run: **5.6m** per\n- 5 or more Runs: **5.2m** per",

        color=discord.Color.green()
    )
    embed9.set_thumbnail(
        url="https://i.postimg.cc/FRs6KzJC/livid.webp")
    embed9.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed10 = discord.Embed(
        title="<:sadan:1205283244312895488>Master Mode 6",
        description="**S Runs**\n- 1 run: **7.5m** per\n- 5 or more Runs: **6.7m** per",

        color=discord.Color.green()
    )
    embed10.set_thumbnail(
        url="https://i.postimg.cc/0NC3xDrJ/sadan.webp")
    embed10.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed11 = discord.Embed(
        title="<:necron:1205283242698219540>Master Mode 7",
        description="**S Runs**\n- 5 or more Runs: **32m** per\n- 5 or more Runs: **28m** per",

        color=discord.Color.green()
    )
    embed11.set_thumbnail(
        url="https://i.postimg.cc/hGnwHp4B/necron.webp")
    embed11.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed12 = discord.Embed(
        title="Требования",
        description="Пожалуйста, убедитесь, что ваш уровень катакомб соответсвует выбранному Master Mode Floor при создании тикета. Требования следующие:\n\n▬▬▬▬▬▬▬▬\nMaster Mode 1 требует Catacombs level 24\nMaster Mode 2 требует Catacombs level 26\nMaster Mode 3 требует Catacombs level 28\nMaster Mode 4 требует Catacombs level 30\nMaster Mode 5 требует Catacombs level 32\nMaster Mode 6 требует Catacombs level 34\nMaster Mode 7 требует Catacombs level 36\n\n**Примечание:** Для перехода на этаж, для которого вы покупаете керри, необходимо пройти предыдущие этажи Master Mode, если такие имеются.",

        color=discord.Color.green()
    )
    embed12.set_thumbnail(
        url="https://i.postimg.cc/CMJHpcKH/moose-moosecraft.gif")
    embed12.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed13 = discord.Embed(
        title="Опыт",
        description="Это стандартный опыт, который вы точно получите, за прохождение на S ранг. Вы можете получить на 10% больше опыта, если у вас есть Catacombs Expert Ring, и до 50% больше опыта, если у вас больше 25-ти пройденных в Master Mode этажей\n\n▬▬▬▬▬▬▬▬\nMaster Mode 1 — 9k\nMaster Mode 2 — 13k\nMaster Mode 3 — 33k\nMaster Mode 4 — 55k\nMaster Mode 5 — 60k\nMaster Mode 6 — 85k\nMaster Mode 7 — 400k",

        color=discord.Color.green()
    )
    embed13.set_thumbnail(
        url="https://i.postimg.cc/nLvBRk5m/whoa-oh.gif")
    embed13.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed14 = discord.Embed(
        title="Dungeon Services (Master Mode)",
        description="<:bonzo:1205283252487716924>_ _ Master Mode 1\n<:scarf:1205283251003072543> _ _ Master Mode 2\n<:professor:1205283249572675594> _ _ Master Mode 3\n<:Thorn:1205283247903211730> _ _ Master Mode 4\n<:livid:1205283246099660810> _ _ Master Mode 5\n<:sadan:1205283244312895488> _ _ Master Mode 6\n<:necron:1205283242698219540> _ _ Master Mode 7",

        color=discord.Color.green()
    )
    embed14.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed14.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed15 = discord.Embed(
        title="Marvelous Elite Forces Rules",
        description="**Все правила на сервере работают всегда и везде. Если вы нарушите правило, вы получите наказание.**\n\n- **1. Будьте уважительны ко всем членам гильдии и относитесь ко всем одинаково. Независимо от пола, религии или расы.**\n - Если у вас есть личные претензии к ним, пожалуйста, решайте их в личных сообщениях.\n\n- **2. Без расизма.**\n - Расовые высказывания любого рода, включая шутки, строго запрещены на сервере. Мы придерживаемся политики нетерпимости к расизму и будем принимать жесткие меры против него.\n\n- **3. Не спамить.**\n - Если вы будете пойманы на спаме, это приведет к муту или бану на сервере. (Это включает, но не ограничивается пингами, капсом, чатволлом или спамом эмодзи).\n - Чрезмерное использование функций markdown, нарушающее течение чата или спам, строго запрещено. Это включает в себя, но не ограничивается чрезмерным использованием, созданием цепочек из элементов markdown, заслонением чата и спамом с помощью элементов markdown.\n\n- **4. Прямые и косвенные угрозы.**\n - Угрозы другим пользователям DDoS, Death, DoX, оскорбления и другие вредоносные угрозы категорически запрещены и не допускаются.\n - Шутки на подобную тему также могут повлечь за собой наказание.\n\n- **5. Никакого NSFW-контента.**\n - Это сервер сообщества, и он не предназначен для обмена материалами такого рода. (NSFW-контент определяется по усмотрению персонала)\n\n- **6. Обсуждение политики и религии не приветствуется**\n\n- **7. Соблюдайте [правила сообщества Discord](https://discord.com/guidelines) и [условия обслуживания](https://discord.com/terms).**\n - Если вы не будете соблюдать правила и условия обслуживания, это приведет к муту или бану в зависимости от степени тяжести.\n\n- **8. Никакой рекламы.**\n - Это касается серверов Discord, гильдий, видео на Youtube, наших официальных сервисов или любого рода контента.\n\n- **9. Русскйй и англоязычный канал.**\n\n- **10. Попытки выдать себя за сотрудников нашего сервера или команды персонала приведут к перманентному бану.**\n\n- **11. Не пинговать следующие роли и людей с данными ролями.**\n - <@&1197859705033326633>|<@&1203739269206773890>|<@&1203739272402964592>|<@&1205068967438188574>|<@&1196442304488153139>|@here\n\n- **12. Видеоконтент, признанный вредоносным, запрещен.**\n - Это включает в себя любой обход Автомода или других правил.\n\n- **13. Не публикуйте дискорд-крашеры ни в одном канале. Их размещение приведет к временному бану.**\n\n- **14. Мошенничество и потоковые читы могут привести к бану.**\n - Это зависит от истории ваших наказаний.\n - Мы следуем всем правилам гильдии Hypixel. С правилами Hypixel вы можете ознакомиться [здесь](https://hypixel.net/rules).\n\n- **15. Используйте каналы соответствующим образом.**\n - Вы не должны использовать каналы не по их прямому назначению.\n\n- **16. Если вы занижаете цену или пытаетесь продать наши официальные услуги в любом виде, вы будете забанены.**\n - Это касается и других серверов.\n\n***Сотрудники гильдии оставляют за собой право варнить, мутить или банить за проступки/ситуации, не указанные в явном виде. Пользуйтесь здравым смыслом.***\n\nДлительность всех наказаний определяется сотрудниками гильдии по своему усмотрению.\n Все эти правила действуют в текстовых и голосовых каналах.\n\nВступая на сервер, вы соглашаетесь и подтверждаете, что ознакомились с правилами. Администрация оставляет за собой право удалить вас с сервера в любое время по любой причине. Непрочтение правил не освобождает вас от ответственности.",

        color=discord.Color.green()
    )
    embed15.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed15.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed16 = discord.Embed(
        title="Условия предоставления услуг",
        description="**1)** Не создавайте тикет на керри, если вы не готовы получить услугу.\n**2)** Оплата производится авансом без исключений.\n**3)** Если вы умрете более 2 раз и приведете к снижению счета по сравнению с тем, который вы заказали, мы не обязаны компенсировать вашу потерю.\n**4)** Если вы отключитесь во время керри, тот кто делает вам керри попытается отправить вас обратно. Если вы не сможете вернуться, у вас будет 48 часов, чтобы забрать монеты, иначе они останутся у человека, который вам делал керри.\n**5)** Как только вы войдете в Катакомбы, выбранный вами класс будет зависеть от принявшего ваш тикет человека, чтобы керри было более эффективное.\n**6)** Ваш керри считается оконченным, когда вы наберете заказанное количество прохождения того или иного этажа.\n**7)** Весь лут, который вы получите, полностью ваш.\n**8)** Вам не разрешается приглашать других людей на керри. Когда вы платите за керри, вы платите за себя, а не за себя и того, кого вы хотите пригласить. Однако вы можете пригласить других людей, если вы также заплатите за каждого дополнительного человека в партии.\n**9)** Указанные цены не подлежат обсуждению, попытка занизить цену приведет к варну.\n**10)** Не пингуйте членов сервисной команды в вашем тикете, терпеливо ждите, пока кто-нибудь не заберет ваш тикет.\n\n__**Примечания**__\n\n- Вы получите варн за нарушение любого из вышеперечисленных правил.\n- Если у вас будет 5 варнов, вы получите черный список тикетов и не сможете открыть ни одного тикета.",

        color=discord.Color.green()
    )
    embed16.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed16.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed17 = discord.Embed(
        title="<:Thorn:1205283247903211730>Floor 4",
        description="",

        color=discord.Color.green()
    )
    embed17.add_field(name="Completion", value="- 1 Run: **400k** per\n- 5 or more Runs: **350k** per", inline=True)
    embed17.add_field(name="S Runs", value="- 1 Run: **600k** per\n- 5 or more Runs: **550k** per", inline=True)
    embed17.add_field(name="S+ Runs", value="- 1 Run: **950k** per\n- 5 or more Runs: **900k** per", inline=True)
    embed17.set_thumbnail(
        url="https://i.postimg.cc/WzdfMy8M/Thorn.webp")
    embed17.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed18 = discord.Embed(
        title="<:livid1:1206195590464147526>Floor 5",
        description="",

        color=discord.Color.green()
    )
    embed18.add_field(name="Completion", value="- 1 Run: **450k** per\n- 5 or more Runs: **400k** per", inline=True)
    embed18.add_field(name="S Runs", value="- 1 Run: **600k** per\n- 5 or more Runs: **500k** per", inline=True)
    embed18.add_field(name="S+ Runs", value="- 1 Run: **1m** per\n- 5 or more Runs: **900k** per", inline=True)
    embed18.set_thumbnail(
        url="https://i.postimg.cc/cH5rLKgT/759298251068801044.png")
    embed18.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed19 = discord.Embed(
        title="<:sadan:1205283244312895488>Floor 6",
        description="",

        color=discord.Color.green()
    )
    embed19.add_field(name="Completion", value="- 1 Run: **700k** per\n- 5 or more Runs: **600k** per", inline=True)
    embed19.add_field(name="S Runs", value="- 1 Run: **900k** per\n- 5 or more Runs: **850k** per", inline=True)
    embed19.add_field(name="S+ Runs", value="- 1 Run: **1.4m** per\n- 5 or more Runs: **1.2m** per", inline=True)
    embed19.set_thumbnail(
        url="https://i.postimg.cc/0NC3xDrJ/sadan.webp")
    embed19.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed20 = discord.Embed(
        title="<:necron:1205283242698219540>Floor 7",
        description="",

        color=discord.Color.green()
    )
    embed20.add_field(name="Completion", value="- 1 Run: **4m** per\n- 5 or more Runs: **3.5m** per", inline=True)
    embed20.add_field(name="S Runs", value="- 1 Run: **7.5m** per\n- 5 or more Runs: **7m** per", inline=True)
    embed20.add_field(name="S+ Runs", value="- 1 Run: **12m** per\n- 5 or more Runs: **10m** per", inline=True)
    embed20.set_thumbnail(
        url="https://i.postimg.cc/hGnwHp4B/necron.webp")
    embed20.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed21 = discord.Embed(
        title="Требования",
        description="Пожалуйста, убедитесь, что ваш уровень катакомб соответсвует выбранному Master Mode Floor при создании тикета. Требования следующие:\n\n▬▬▬▬▬▬▬▬\nFloor 4 требует Catacombs level 9\nFloor 5 требует Catacombs level 14\nFloor 6 требует Catacombs level 19\nFloor 7 требует Catacombs level 24",

        color=discord.Color.green()
    )
    embed21.set_thumbnail(
        url="https://i.postimg.cc/CMJHpcKH/moose-moosecraft.gif")
    embed21.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed22 = discord.Embed(
        title="Dungeon Carry Services",
        description="<:Thorn:1205283247903211730>_ _ Floor 4\n<:livid1:1206195590464147526>_ _ Floor 5\n<:sadan:1205283244312895488>_ _ Floor 6\n<:necron:1205283242698219540>_ _ Floor 7",

        color=discord.Color.green()
    )
    embed22.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed22.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed23 = discord.Embed(
        title="Условия предоставления услуг",
        description="**1)** Не создавайте тикет на керри, если вы не готовы получить услугу.\n**2)** Попытка обмануть людей, которые керрят вам слеиров, приведет к бану.\n**3)** Оплата производится авансом без исключений.\n**4)** Ваш уровень комбата должен быть выше 20.\n**5)** Если вы погибли из-за собственных ошибок, человек, который делает вам керри. не обязаны переделывать босса за вас. Также вы должны прислушиваться к правилам, которые вам скажет человек, который принял ваш тикет.\n**6)** Любой лут, который вы получите с босса, останется у вас. Это касается и тех случаев, когда вы получаете исключительно редкий дроп.\n**7)** Керри закончится, как только вы получите опыт после смерти босса.\n**8)** Указанные цены не подлежат обсуждению, попытка занизить цену приведет к варну.\n**9)** Не пингуйте членов сервисной команды в вашем тикете, терпеливо ждите, пока кто-нибудь не заберет ваш тикет.\n**10)** Вы можете попросить керри T2/T1, но должны рассчитывать на то, что вам придется заплатить за них как за керри T3.\n\n__**Примечания**__\n\n-  Вы получите варн за нарушение любого из вышеперечисленных правил.\n- Если у вас будет 5 варнов, вы получите черный список тикетов и не сможете открыть ни одного тикета.",

        color=discord.Color.green()
    )
    embed23.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed23.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed24 = discord.Embed(
        title="Требования",
        description="- Обратите внимание, что перед заказом какоголибо уровня вы должны убить слеира предыдущего уровня. Это означает, что перед заказом 3-го уровня вы должны убить хотя бы одного 2-го уровня. Перед заказом 4-го уровня вы должны убить хотя бы одного 3-го уровня. Кроме того, убедитесь, что у вас есть хотя бы 21-й уровень комбата, чтобы вы могли войти в Zealot Bruiser Hideout.\n- Если вы заказываете ревенанта 5-ого уровня, убедитесь, что ваш комбат уровень 25, уровень сеира ревенантов 7 и вы убили хотя бы одного босса ревенанта четвертого уровня. В противном случае вы получите варн.",

        color=discord.Color.green()
    )
    embed24.set_thumbnail(
        url="https://i.postimg.cc/CMJHpcKH/moose-moosecraft.gif")
    embed24.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed25 = discord.Embed(
        title="<a:blaze:1206280782726045717> _ _ Blaze Slayer",
        description="- Inferno Demonlord Tier 2: **1.5m** per\n- 5 or more: **1.2m** per\n\n- Inferno Demonlord Tier 3: **3m** per\n- 5 or more: **2.5m** per\n\n- Inferno Demonlord Tier 4: **6m** per\n- 5 or more: **5m** per\n\nПожалуйста, обратите внимание на то, что при покупке слеиров блейзов настоятельно рекомендуется иметь не менее 3/4 sorrow, чтобы помочь вам выжить на боссе!",

        color=discord.Color.green()
    )
    embed25.set_thumbnail(
        url="https://i.postimg.cc/Vv13SJmx/blaze.gif")
    embed23.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed26 = discord.Embed(
        title="<a:Enderman:1206280777503866950> _ _ Enderman Slayer",
        description="- Voidgloom Seraph 3: **1m** per\n- 5 or more: **800k** per\n\n- Voidgloom Seraph 4: **2.5m** per\n- 5 or more: **2m** per",

        color=discord.Color.green()
    )
    embed26.set_thumbnail(
        url="https://i.postimg.cc/Z5VKJhFY/Enderman.gif")
    embed26.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed27 = discord.Embed(
        title="<:revenant:1206280774958186518> _ _ T5 Rev",
        description="- Atoned Horror: **200k** per\n- 5 or more: **150k** per",

        color=discord.Color.green()
    )
    embed27.set_thumbnail(
        url="https://i.postimg.cc/fWpdhYWq/revenant.png")
    embed27.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed28 = discord.Embed(
        title="Slayer Carry Service",
        description="<a:blaze:1206280782726045717>_ _ Inferno Demonlord Carry Service\n<a:Enderman:1206280777503866950>_ _ Voidgloom Seraph Carry Service\n<:revenant:1206280774958186518>_ _ Revenant Horror Carry Service",

        color=discord.Color.green()
    )
    embed28.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed28.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed29 = discord.Embed(
        title="Условия предоставления услуг",
        description="**1)** Не создавайте тикет на керри, если вы не готовы получить услугу.\n**2)** Попытка обмануть людей, которые керрят вам куудру, приведет к бану.\n**3)** Оплата производится авансом без исключений.\n**4)** Ваш уровень комбата должен быть выше 24.\n**5)** Любой лут, который вы получите с босса, останется у вас. Это касается и тех случаев, когда вы получаете исключительно редкий дроп.\n**6)** Керри закончится, как только вы получите опыт после смерти босса.\n**7)** Указанные цены не подлежат обсуждению, попытка занизить цену приведет к варну.\n**8)** Не пингуйте членов сервисной команды в вашем тикете, терпеливо ждите, пока кто-нибудь не заберет ваш тикет.\n\n__**Примечания**__\n\n- Вы получите варн за нарушение любого из вышеперечисленных правил.\n- Если у вас будет 5 варнов, вы получите черный список тикетов и не сможете открыть ни одного тикета.",

        color=discord.Color.green()
    )
    embed29.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed29.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed30 = discord.Embed(
        title="Требования",
        description="- Basic Tier - завершенить квест.\n- Hot Tier - 1000 репутации\n- Burning Tier - 3000 репутации\n- Fiery Tier - 7000 репутации\n- Infernal Tier - 12000 репутации",

        color=discord.Color.green()
    )
    embed30.set_thumbnail(
        url="https://i.postimg.cc/CMJHpcKH/moose-moosecraft.gif")
    embed30.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed31 = discord.Embed(
        title="<:Basic:1206649051626602596> _ _ Basic Tier",
        description="- 1 Run: **6m** per\n- 3 or more Runs: **4m** per",

        color=discord.Color.green()
    )
    embed31.set_thumbnail(
        url="https://i.postimg.cc/SR0Xkv1D/Basic.png")
    embed31.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed32 = discord.Embed(
        title="<:Hot:1206649049311350814> _ _ Hot Tier",
        description="- 1 Run: **8m** per\n- 3 or more Runs: **6m** per",

        color=discord.Color.green()
    )
    embed32.set_thumbnail(
        url="https://i.postimg.cc/FHP77Rnf/Hot.png")
    embed32.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed33 = discord.Embed(
        title="<:Burning:1206649047520124958> _ _ Burning Tier",
        description="- 1 Run: **14m** per\n- 3 or more Runs: **11m** per",

        color=discord.Color.green()
    )
    embed33.set_thumbnail(
        url="https://i.postimg.cc/D0qSZPtF/Burning.png")
    embed33.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed34 = discord.Embed(
        title="<:Fiery:1206649045691535450> _ _ Fiery Tier",
        description="- 1 Run: **19m** per\n- 3 or more Runs: **15m** per",

        color=discord.Color.green()
    )
    embed34.set_thumbnail(
        url="https://i.postimg.cc/Fs4f6wLK/Fiery.png")
    embed34.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed35 = discord.Embed(
        title="<:Infernal:1206649043489394688> _ _ Infernal Tier",
        description="- 1 Run: **40m** per\n- 3 or more Runs: **33m** per",

        color=discord.Color.green()
    )
    embed35.set_thumbnail(
        url="https://i.postimg.cc/0NFj04vP/Infernal.png")
    embed35.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed36 = discord.Embed(
        title="Kuudra Carry Service",
        description="<:Basic:1206649051626602596>_ _ Kuudra Basic Tier Carry Service\n<:Hot:1206649049311350814>_ _ Kuudra Hot Tier Carry Service\n<:Burning:1206649047520124958>_ _ Kuudra Burning Carry Service\n<:Fiery:1206649045691535450>_ _ Kuudra Fiery Tier Carry Service\n<:Infernal:1206649043489394688>_ _ Kuudra Infernal Tier Carry Service",

        color=discord.Color.green()
    )
    embed36.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed36.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed37 = discord.Embed(
        title="Условия предоставления услуг",
        description="**1)** Не создавайте тикет на керри, если вы не готовы получить услугу.\n**2)** Вы должны сначала передать деньги зельевару, а затем получить зелья.\n**3)** Если пивовар просит вас заплатить больше установленной цены, сообщите об этом в <#1201205857011105863>. Вы также можете сообщить о них, если они вас обманывают.\n**4)** Указанные цены не подлежат обсуждению, попытка занизить цену приведет к варну.\n**5)** Не пингуйте членов сервисной команды в вашем тикете, терпеливо ждите, пока кто-нибудь не заберет ваш тикет.\n\n__**Примечания**__\n\n- Вы получите варн за нарушение любого из вышеперечисленных правил.\n- Если у вас будет 5 варнов, вы получите черный список тикетов и не сможете открыть ни одного тикета.",

        color=discord.Color.green()
    )
    embed37.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed37.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed38 = discord.Embed(
        title="<a:potion:1207402670546227301> _ _ Brewing Service",
        description="",

        color=discord.Color.green()
    )
    embed38.add_field(name="15x Haste Potions: 500k", value="- Level 3\n- Splashables\n- 24 Minutes Long", inline=True)
    embed38.add_field(name="15x Rabbit Potions: 500k", value="- Level 5\n- Splashables\n- 24 Minutes Long", inline=True)
    embed38.add_field(name="15x Experience Potions: 800k", value="- Level 1\n- Splashables\n- With Viking Tear (10% more Combat XP)\n- 24 Minutes Long", inline=True)
    embed38.add_field(name="15x Archery Potions: 1.4m", value="- Level 4\n- Splashables\n- With Tutti Frutti (5% More Damage)\n- 24 Minutes Long", inline=False)
    embed38.add_field(name="15x Combat XP Boost Potions: 5m", value="- Level 3\n- Splashables\n- 54 Minutes Long", inline=True)
    embed38.add_field(name="Цена оптового заказа", value="Только при покупке 300 или более зелий любого типа. Скидка составляет 10%.", inline=True)
    embed38.set_thumbnail(
        url="https://i.postimg.cc/Rhk3cq7m/po-ao-minecraft.gif")
    embed38.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed39 = discord.Embed(
        title="Brewing Service",
        description="<a:potion:1207402670546227301> _ _ Brewing Service",

        color=discord.Color.green()
    )
    embed39.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed39.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    embed = discord.Embed(
        title="Добро пожаловать в Marvelous Elite Forces",
        description="Вы можете привязать свою учетную запись Minecraft, если хотите получить доступ к:\n\n"
                    "- Помощь в прохождении этажей катакомб\n- Получить возможность вступить в гильдию\n- Получить помощь от опытного русского комьюнити\n\n Также вы можете получить привелегию, которая у вас есть на аккаунте. \n\nЕсли у вас возникли проблемы, создайте тикет в канале <#1201205857011105863>.\tМы будем рады вам помочь.",


        color=discord.Color.green()
    )
    embed.set_thumbnail(
        url="https://i.postimg.cc/9FH3tx4X/standard.gif")
    embed.set_footer(text="MEF Bot by snowdrop6666", icon_url="https://i.postimg.cc/P5PHMc7h/wasd.png")


    view = StartVerificationView()
    view2 = InformationView()
    view3 = MasterModeView()

    await channel.send(embed=embed, view=view)
    await channel1.send(embed=embed1)
    await channel2.send(embed=embed2, view=view2)
    await channel3.send(embed=embed3)
    await channel4.send(embed=embed4)
    await channel4.send(embed=embed5)
    await channel4.send(embed=embed6)
    await channel4.send(embed=embed7)
    await channel4.send(embed=embed8)
    await channel4.send(embed=embed9)
    await channel4.send(embed=embed10)
    await channel4.send(embed=embed11)
    await channel4.send(embed=embed12)
    await channel4.send(embed=embed13)
    await channel4.send(embed=embed14, view=view3)
    await channel6.send(embed=embed15)
    await channel5.send(embed=embed16)
    await channel5.send(embed=embed17)
    await channel5.send(embed=embed18)
    await channel5.send(embed=embed19)
    await channel5.send(embed=embed20)
    await channel5.send(embed=embed21)
    await channel5.send(embed=embed22)
    await channel7.send(embed=embed23)
    await channel7.send(embed=embed24)
    await channel7.send(embed=embed25)
    await channel7.send(embed=embed26)
    await channel7.send(embed=embed27)
    await channel7.send(embed=embed28)
    await channel8.send(embed=embed29)
    await channel8.send(embed=embed30)
    await channel8.send(embed=embed31)
    await channel8.send(embed=embed32)
    await channel8.send(embed=embed33)
    await channel8.send(embed=embed34)
    await channel8.send(embed=embed35)
    await channel8.send(embed=embed36)
    await channel9.send(embed=embed37)
    await channel9.send(embed=embed38)
    await channel9.send(embed=embed39)

@bot.event
async def on_ready():
    print(f'{bot.user} возобновил работу!')

    await bot.tree.sync()

    await embedinf()

bot.run(BOT_TOKEN)