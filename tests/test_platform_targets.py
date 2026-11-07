import zipfile

from fleasion.modifications import platform_targets
from fleasion.modifications.manager import ModificationManager
from fleasion.utils import platform_linux


def test_linux_sober_resource_target_maps_pc_sky_to_android(tmp_path, monkeypatch):
    monkeypatch.setattr(platform_targets.sys, "platform", "linux")
    monkeypatch.setattr(
        platform_targets,
        '_linux_resource_client_key',
        lambda _resource_dir: 'sober',
    )

    assert platform_targets.target_path_for_resource_dir(
        r"PlatformContent\pc\textures\sky\sky512_bk.tex",
        tmp_path / 'sober-resources',
    ) == "android/textures/sky/sky512_bk.tex"


def test_linux_resource_target_seam_preserves_logical_content_paths(tmp_path, monkeypatch):
    monkeypatch.setattr(platform_targets.sys, 'platform', 'linux')
    monkeypatch.setattr(
        platform_targets,
        '_linux_resource_client_key',
        lambda _resource_dir: 'future',
    )
    resource_root = tmp_path / 'future-client' / 'resources'

    assert platform_targets.target_path_for_resource_dir(
        r'content\sounds\oof.ogg', resource_root
    ) == 'content/sounds/oof.ogg'
    assert platform_targets.target_path_for_resource_dir(
        r'PlatformContent\pc\textures\sky\sky512_bk.tex', resource_root
    ) == 'PlatformContent/pc/textures/sky/sky512_bk.tex'


def test_non_linux_target_path_keeps_existing_storage_form(monkeypatch):
    monkeypatch.setattr(platform_targets.sys, "platform", "win32")

    assert platform_targets.target_path_for_current_platform(
        r"PlatformContent\pc\textures\sky\sky512_bk.tex"
    ) == r"PlatformContent\pc\textures\sky\sky512_bk.tex"


def test_read_linux_sober_original_asset_from_apk(tmp_path, monkeypatch):
    sober_data = tmp_path / "sober"
    apk = sober_data / "packages" / "x86_64" / "com.roblox.client" / "base.apk"
    apk.parent.mkdir(parents=True)
    with zipfile.ZipFile(apk, "w") as archive:
        archive.writestr("assets/android/textures/sky/sky512_bk.tex", b"sky")

    monkeypatch.setattr(platform_targets.sys, "platform", "linux")
    monkeypatch.setattr(platform_linux, "SOBER_DATA_DIR", sober_data)
    monkeypatch.setattr(platform_linux, "SOBER_LEGACY_EXE_DIR", sober_data / "exe")
    monkeypatch.setattr(
        platform_linux,
        "selected_linux_client_key",
        lambda: "sober",
    )

    assert platform_targets.read_current_platform_original_asset(
        r"PlatformContent\pc\textures\sky\sky512_bk.tex"
    ) == b"sky"


def test_modification_manager_migrates_saved_sober_path_to_logical_target(monkeypatch):
    monkeypatch.setattr(platform_targets.sys, "platform", "linux")
    manager = ModificationManager.__new__(ModificationManager)
    manager._data = {
        "entries": [
            {
                "target_path": "android/textures/sky/sky512_bk.tex",
                "source_type": "local_file",
            }
        ]
    }

    assert manager._migrate_target_paths_for_current_platform() is True
    assert manager._data["entries"][0]["target_path"] == (
        "PlatformContent/pc/textures/sky/sky512_bk.tex"
    )


def test_read_linux_sober_original_directory_from_apk(tmp_path, monkeypatch):
    sober_data = tmp_path / 'sober'
    apk = sober_data / 'packages' / 'x86_64' / 'com.roblox.client' / 'base.apk'
    apk.parent.mkdir(parents=True)
    with zipfile.ZipFile(apk, 'w') as archive:
        archive.writestr('assets/content/fonts/families/BuilderSans.json', b'{"faces": []}')
        archive.writestr('assets/content/fonts/families/Arimo.json', b'{"faces": []}')
        archive.writestr('assets/content/fonts/families/nested/ignored.json', b'{}')

    monkeypatch.setattr(platform_targets.sys, 'platform', 'linux')
    monkeypatch.setattr(platform_linux, 'SOBER_DATA_DIR', sober_data)
    monkeypatch.setattr(platform_linux, 'SOBER_LEGACY_EXE_DIR', sober_data / 'exe')
    monkeypatch.setattr(
        platform_targets,
        '_linux_resource_client_key',
        lambda _resource_dir: 'sober',
    )

    result = platform_targets.read_current_platform_original_directory(
        'content/fonts/families',
        resource_dir=tmp_path / 'asset_overlay',
    )

    assert result == {
        'Arimo.json': b'{"faces": []}',
        'BuilderSans.json': b'{"faces": []}',
    }


def test_linux_mocktail_resource_target_maps_pc_sky_to_android(tmp_path, monkeypatch):
    monkeypatch.setattr(platform_targets.sys, "platform", "linux")
    monkeypatch.setattr(
        platform_targets,
        '_linux_resource_client_key',
        lambda _resource_dir: 'mocktail',
    )

    assert platform_targets.target_path_for_resource_dir(
        r"PlatformContent\pc\textures\sky\sky512_bk.tex",
        tmp_path / 'mocktail-resources',
    ) == "android/textures/sky/sky512_bk.tex"


def test_linux_target_path_candidates_for_current_platform_includes_mocktail(monkeypatch):
    monkeypatch.setattr(platform_targets.sys, "platform", "linux")

    candidates = platform_targets.target_path_candidates_for_current_platform(
        r"PlatformContent\pc\textures\sky\sky512_bk.tex"
    )

    assert "android/textures/sky/sky512_bk.tex" in candidates
    assert "PlatformContent/pc/textures/sky/sky512_bk.tex" in candidates


def test_read_linux_mocktail_original_asset_from_apk(tmp_path, monkeypatch):
    mocktail_data = tmp_path / "mocktail"
    apk = mocktail_data / "packages" / "x86_64" / "com.roblox.client" / "base.apk"
    apk.parent.mkdir(parents=True)
    with zipfile.ZipFile(apk, "w") as archive:
        archive.writestr("assets/android/textures/sky/sky512_bk.tex", b"sky")

    monkeypatch.setattr(platform_targets.sys, "platform", "linux")
    monkeypatch.setattr(platform_linux, "MOCKTAIL_DATA_DIR", mocktail_data)
    monkeypatch.setattr(platform_linux, "MOCKTAIL_LEGACY_EXE_DIR", mocktail_data / "exe")
    monkeypatch.setattr(
        platform_linux,
        "selected_linux_client_key",
        lambda: "mocktail",
    )

    assert platform_targets.read_current_platform_original_asset(
        r"PlatformContent\pc\textures\sky\sky512_bk.tex"
    ) == b"sky"


def test_read_linux_mocktail_original_asset_from_payload_assets(tmp_path, monkeypatch):
    mocktail_data = tmp_path / "mocktail"
    assets = mocktail_data / "payloads" / "1234-abcdef" / "assets" / "content"
    assets.mkdir(parents=True)
    (assets / "android" / "textures" / "sky").mkdir(parents=True)
    (assets / "android" / "textures" / "sky" / "sky512_bk.tex").write_bytes(b"sky")
    (mocktail_data / "current.json").write_text(
        '{"payload_id": "1234-abcdef"}', encoding='utf-8'
    )

    monkeypatch.setattr(platform_targets.sys, "platform", "linux")
    monkeypatch.setattr(platform_linux, "MOCKTAIL_DATA_DIR", mocktail_data)
    monkeypatch.setattr(platform_linux, "MOCKTAIL_LEGACY_EXE_DIR", mocktail_data / "exe")
    monkeypatch.setattr(
        platform_linux,
        "selected_linux_client_key",
        lambda: "mocktail",
    )

    assert platform_targets.read_current_platform_original_asset(
        r"PlatformContent\pc\textures\sky\sky512_bk.tex"
    ) == b"sky"


def test_read_linux_mocktail_original_directory_from_apk(tmp_path, monkeypatch):
    mocktail_data = tmp_path / 'mocktail'
    apk = mocktail_data / 'packages' / 'x86_64' / 'com.roblox.client' / 'base.apk'
    apk.parent.mkdir(parents=True)
    with zipfile.ZipFile(apk, 'w') as archive:
        archive.writestr('assets/content/fonts/families/BuilderSans.json', b'{"faces": []}')
        archive.writestr('assets/content/fonts/families/Arimo.json', b'{"faces": []}')
        archive.writestr('assets/content/fonts/families/nested/ignored.json', b'{}')

    monkeypatch.setattr(platform_targets.sys, 'platform', 'linux')
    monkeypatch.setattr(platform_linux, 'MOCKTAIL_DATA_DIR', mocktail_data)
    monkeypatch.setattr(platform_linux, 'MOCKTAIL_LEGACY_EXE_DIR', mocktail_data / 'exe')
    monkeypatch.setattr(
        platform_targets,
        '_linux_resource_client_key',
        lambda _resource_dir: 'mocktail',
    )

    result = platform_targets.read_current_platform_original_directory(
        'content/fonts/families',
        resource_dir=tmp_path / 'asset_overlay',
    )

    assert result == {
        'Arimo.json': b'{"faces": []}',
        'BuilderSans.json': b'{"faces": []}',
    }
