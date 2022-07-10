from create_bot import dp
from aiogram import executor
from headers import client, admin


def main():

    client.register_client_message(dp)
    admin.register_admin_message(dp)

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
