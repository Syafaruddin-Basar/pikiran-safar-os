# core_ledger/models/financial_core.py

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class AccountType(enum.Enum):
    ASSET = "Asset"
    LIABILITY = "Liability"
    EQUITY = "Equity"
    REVENUE = "Revenue"
    EXPENSE = "Expense"

class Entity(Base):
    """
    Merepresentasikan unit legal atau operasional.
    Tidak ada cross-entity mutation tanpa settlement engine.
    """
    __tablename__ = 'entities'

    entity_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    parent_entity_id = Column(UUID(as_uuid=True), ForeignKey('entities.entity_id'), nullable=True)
    jurisdiction_id = Column(String(100), nullable=False)
    risk_appetite_profile_id = Column(String(100), nullable=False)
    capital_buffer_id = Column(String(100), nullable=False)
    status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    version = Column(Integer, default=1, nullable=False)

    # Relasi
    parent = relationship("Entity", remote_side=[entity_id])
    accounts = relationship("Account", back_populates="entity")
    ledgers = relationship("Ledger", back_populates="entity")

class Account(Base):
    """
    Struktur chart of accounts.
    Account tidak pernah dihapus. Hanya dinonaktifkan.
    """
    __tablename__ = 'accounts'

    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), ForeignKey('entities.entity_id'), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    currency_id = Column(String(10), nullable=False)
    parent_account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.account_id'), nullable=True)
    risk_category = Column(String(100), nullable=False)
    liquidity_class = Column(String(50), nullable=False)
    active_flag = Column(Boolean, default=True, nullable=False)

    # Relasi
    entity = relationship("Entity", back_populates="accounts")
    parent = relationship("Account", remote_side=[account_id])

class Ledger(Base):
    """
    Ledger adalah container event-sourced untuk satu entity.
    Ledger period yang sudah ditutup tidak bisa diubah.
    """
    __tablename__ = 'ledgers'

    ledger_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), ForeignKey('entities.entity_id'), nullable=False)
    opening_balance_hash = Column(String(256), nullable=False)
    closing_balance_hash = Column(String(256), nullable=True)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    locked_flag = Column(Boolean, default=False, nullable=False)

    # Relasi
    entity = relationship("Entity", back_populates="ledgers")
    journal_entries = relationship("JournalEntry", back_populates="ledger")

class TransactionEvent(Base):
    """
    Event source layer. Semua perubahan ledger harus berasal dari event.
    """
    __tablename__ = 'transaction_events'

    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String(100), nullable=False)
    source_system = Column(String(100), nullable=False)
    decision_reference_id = Column(String(255), nullable=True)
    authority_signature_hash = Column(String(256), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    event_hash = Column(String(256), nullable=False)

    # Relasi
    journal_entries = relationship("JournalEntry", back_populates="event")

class JournalEntry(Base):
    """
    Representasi transaksi tingkat atas.
    Total Debit = Total Credit (hard constraint).
    """
    __tablename__ = 'journal_entries'

    journal_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ledger_id = Column(UUID(as_uuid=True), ForeignKey('ledgers.ledger_id'), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey('transaction_events.event_id'), nullable=False)
    transaction_type = Column(String(100), nullable=False)
    approval_status = Column(String(50), nullable=False)
    total_debit = Column(Integer, nullable=False) 
    total_credit = Column(Integer, nullable=False)
    created_by = Column(String(100), nullable=False)
    approved_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relasi
    ledger = relationship("Ledger", back_populates="journal_entries")
    event = relationship("TransactionEvent", back_populates="journal_entries")
    lines = relationship("JournalLine", back_populates="journal")

class JournalLine(Base):
    """
    Detail per akun.
    """
    __tablename__ = 'journal_lines'

    line_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    journal_id = Column(UUID(as_uuid=True), ForeignKey('journal_entries.journal_id'), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.account_id'), nullable=False)
    debit_amount = Column(Integer, default=0, nullable=False)
    credit_amount = Column(Integer, default=0, nullable=False)
    currency_id = Column(String(10), nullable=False)
    fx_rate_reference = Column(String(100), nullable=True)
    risk_tag = Column(String(100), nullable=False)

    # Relasi
    journal = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account")