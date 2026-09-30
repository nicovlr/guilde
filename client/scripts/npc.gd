extends Area2D

@export var npc_id: String = "npc-1"
@export var display_name: String = "PNJ"

signal interacted(npc_id: String, display_name: String)

var _player_near := false

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)

func _process(_delta: float) -> void:
	if _player_near and Input.is_action_just_pressed("interact"):
		interacted.emit(npc_id, display_name)

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		_player_near = true

func _on_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		_player_near = false
