"""Regression tests for Drive file fidelity gaps fixed in #1016.

Issue: capabilities held only 12 of the 35 keys real answers, and no file
carried permissions.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backlot.routers.google import _CAPABILITIES_EXTRA


# The 35 capability keys real Drive answers on every file (measured 2026-10-25).
_REAL_CAPABILITIES = {
    # 12 keys Backlot already had
    "canAddChildren",
    "canComment",
    "canCopy",
    "canDelete",
    "canDownload",
    "canEdit",
    "canListChildren",
    "canModifyContent",
    "canReadRevisions",
    "canRename",
    "canShare",
    "canTrash",
    # 23 keys added by this fix
    "canAcceptOwnership",
    "canAccessViaGenAi",
    "canAddMyDriveParent",
    "canChangeCopyRequiresWriterPermission",
    "canChangeItemDownloadRestriction",
    "canChangeSecurityUpdateEnabled",
    "canChangeViewersCanCopyContent",
    "canDisableInheritedPermissions",
    "canEnableInheritedPermissions",
    "canModifyContentRestriction",
    "canModifyEditorContentRestriction",
    "canModifyLabels",
    "canModifyOwnerContentRestriction",
    "canMoveChildrenWithinDrive",
    "canMoveItemIntoTeamDrive",
    "canMoveItemOutOfDrive",
    "canMoveItemWithinDrive",
    "canReadLabels",
    "canRemoveChildren",
    "canRemoveContentRestriction",
    "canRemoveMyDriveParent",
    "canStartApproval",
    "canUntrash",
}


def test_capabilities_extra_covers_missing_keys() -> None:
    """_CAPABILITIES_EXTRA must supply all 23 keys absent from the original 12."""
    original_12 = {
        "canAddChildren",
        "canComment",
        "canCopy",
        "canDelete",
        "canDownload",
        "canEdit",
        "canListChildren",
        "canModifyContent",
        "canReadRevisions",
        "canRename",
        "canShare",
        "canTrash",
    }
    missing = _REAL_CAPABILITIES - original_12
    assert set(_CAPABILITIES_EXTRA.keys()) == missing, (
        f"_CAPABILITIES_EXTRA is missing: {missing - set(_CAPABILITIES_EXTRA.keys())}, "
        f"has unexpected: {set(_CAPABILITIES_EXTRA.keys()) - missing}"
    )


def test_capabilities_extra_values_are_bool() -> None:
    """Every value in _CAPABILITIES_EXTRA must be a plain bool."""
    non_bool = {k: v for k, v in _CAPABILITIES_EXTRA.items() if not isinstance(v, bool)}
    assert not non_bool, f"Non-bool capability defaults: {non_bool}"


def test_capabilities_extra_has_23_keys() -> None:
    """Exactly 23 extra keys to bring the total to 35."""
    assert len(_CAPABILITIES_EXTRA) == 23
