from dataclasses import dataclass, field
from enum import StrEnum
import os
import subprocess
from tempfile import TemporaryDirectory, TemporaryFile
from typing import Dict, List, Union

from pandas import isna
from PIL import Image

IMAGE_GENERATOR_PATH = "/Users/henrywilliams/Documents/minesoc/generate-image"


class StructureKind(StrEnum):
    DesertPyramid = "desert_pyramid"
    JunglePyramid = "jungle_pyramid"
    Igloo = "igloo"
    SwampHut = "swamp_hut"
    Village = "village"
    Mansion = "mansion"
    Monument = "monument"
    OceanRuin = "ocean_ruin"
    Shipwreck = "shipwreck"
    BuriedTreasure = "buried_treasure"
    Mineshaft = "mineshaft"
    DesertWell = "desert_well"
    AmethystGeode = "amethyst_geode"
    PillagerOutpost = "pillager_outpost"
    AncientCity = "ancient_city"
    TrailRuins = "trail_ruins"
    TrialChambers = "trial_chambers"
    RuinedPortal = "ruined_portal"
    Spawn = "spawn"
    Stronghold = "stronghold"


@dataclass
class Structure:
    kind: StructureKind
    x: int
    z: int
    details: str

    @classmethod
    def from_dict(cls: "Structure", data: Dict) -> "Structure":
        return cls(
            kind=StructureKind(data["kind"]),
            x=int(data["x"]),
            z=int(data["z"]),
            details=data["details"],
        )


class BiomeKind(StrEnum):
    Badlands = "badlands"
    BambooJungle = "bamboo_jungle"
    Beach = "beach"
    BirchForest = "birch_forest"
    CherryGrove = "cherry_grove"
    ColdOcean = "cold_ocean"
    DarkForest = "dark_forest"
    DeepColdOcean = "deep_cold_ocean"
    DeepFrozenOcean = "deep_frozen_ocean"
    DeepLukewarmOcean = "deep_lukewarm_ocean"
    DeepOcean = "deep_ocean"
    Desert = "desert"
    ErodedBadlands = "eroded_badlands"
    FlowerForest = "flower_forest"
    Forest = "forest"
    FrozenOcean = "frozen_ocean"
    FrozenPeaks = "frozen_peaks"
    FrozenRiver = "frozen_river"
    Grove = "grove"
    IceSpikes = "ice_spikes"
    JaggedPeaks = "jagged_peaks"
    Jungle = "jungle"
    LukewarmOcean = "lukewarm_ocean"
    MangroveSwamp = "mangrove_swamp"
    Meadow = "meadow"
    MushroomFields = "mushroom_fields"
    Ocean = "ocean"
    OldGrowthBirchForest = "old_growth_birch_forest"
    OldGrowthPineTaiga = "old_growth_pine_taiga"
    OldGrowthSpruceTaiga = "old_growth_spruce_taiga"
    Plains = "plains"
    River = "river"
    Savanna = "savanna"
    SavannaPlateau = "savanna_plateau"
    SnowyBeach = "snowy_beach"
    SnowyPlains = "snowy_plains"
    SnowySlopes = "snowy_slopes"
    SnowyTaiga = "snowy_taiga"
    SparseJungle = "sparse_jungle"
    StonyPeaks = "stony_peaks"
    StonyShore = "stony_shore"
    SunflowerPlains = "sunflower_plains"
    Swamp = "swamp"
    Taiga = "taiga"
    WarmOcean = "warm_ocean"
    WindsweptForest = "windswept_forest"
    WindsweptGravellyHills = "windswept_gravelly_hills"
    WindsweptHills = "windswept_hills"
    WindsweptSavanna = "windswept_savanna"
    WoodedBadlands = "wooded_badlands"


@dataclass
class Biome:
    kind: BiomeKind
    count: int

    @classmethod
    def from_dict(cls: "Biome", data: Dict) -> "Biome":
        return cls(kind=BiomeKind(data["kind"]), count=data["count"])


@dataclass
class World:
    seed: int
    structures: List[Structure] = field(default_factory=lambda: [])
    biomes: List[Biome] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.seed = int(self.seed)

    def add_structure(self, kind: str, x: int, z: int, details: str):
        if isna(details):
            details = ""

        self.structures.append(Structure(StructureKind(kind), x, z, details))

    def add_biome(self, kind: str, count: int):
        self.biomes.append(Biome(BiomeKind(kind), count))

    def generate_image(self):
        with TemporaryDirectory() as tmp_dir:
            subprocess.run(
                [
                    IMAGE_GENERATOR_PATH,
                    str(self.seed),
                    os.path.join(tmp_dir, "img.ppm"),
                ],
                check=True,
            )

            subprocess.run(
                [
                    "convert",
                    os.path.join(tmp_dir, "img.ppm"),
                    os.path.join(tmp_dir, "img.png"),
                ],
                capture_output=True,
                check=True,
            )

            return Image.open(os.path.join(tmp_dir, "img.png"))

    def get_structure_count(self, kind: Union[StructureKind, str]) -> int:
        if isinstance(kind, str):
            kind = StructureKind(kind)

        return len(
            [structure for structure in self.structures if structure.kind == kind]
        )

    def get_biome_count(self, kind: Union[BiomeKind, str]) -> int:
        if isinstance(kind, str):
            kind = BiomeKind(kind)

        return [biome for biome in self.biomes if biome.kind == kind][0].count

    @classmethod
    def from_dict(cls: "World", data: Dict) -> "World":
        return cls(
            seed=data["seed"],
            structures=[
                Structure.from_dict(structure) for structure in data["structures"]
            ],
            biomes=[Biome.from_dict(biome) for biome in data["biomes"]],
        )
