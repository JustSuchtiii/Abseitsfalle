import asyncio
import random
import discord
import aiosqlite

from datetime import datetime

DB = "db/tickets.db"

async def ticket_exists(channel_id):
  async with aiosqlite.connect(DB) as db:
    await db.execute(
      "INSERT OR IGNORE INTO tickets (channel_id) VALUES (?)", (channel_id,)
    )
    await db.commit()

async def get_ticket(channel_id):
  async with aiosqlite.connect(DB) as db:
    async with db.execute(
      "SELECT ticket_id FROM tickets WHERE channel_id = ?", (channel_id,)
    ) as cursor:
      ticket = await cursor.fetchone()
  
  return ticket[0]

async def add_ticket(guild_id, channel_id, ticket_id, user_id, version):
  await ticket_exists(channel_id)
  async with aiosqlite.connect(DB) as db:
    await db.execute(
      "UPDATE tickets SET ticket_id = ?, user_id = ?, guild_id = ?, version = ? WHERE channel_id = ?", (ticket_id, user_id, guild_id, version, channel_id)
    )
    await db.commit()

async def remove_ticket(channel_id):
  await ticket_exists(channel_id)
  async with aiosqlite.connect(DB) as db:
    await db.execute(
      "DELETE FROM tickets WHERE channel_id = ?", (channel_id,)
    )
    await db.commit()