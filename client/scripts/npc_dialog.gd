extends Control

const Config = preload("res://scripts/config.gd")

@onready var title_label: Label = $Panel/VBox/Title
@onready var log_label: RichTextLabel = $Panel/VBox/Log
@onready var input_field: LineEdit = $Panel/VBox/HBox/Input
@onready var send_button: Button = $Panel/VBox/HBox/Send
@onready var close_button: Button = $Panel/VBox/Close

var _npc_id: String = ""
var _http: HTTPRequest

func _ready() -> void:
	visible = false
	_http = HTTPRequest.new()
	add_child(_http)
	_http.request_completed.connect(_on_request_completed)
	send_button.pressed.connect(_on_send)
	close_button.pressed.connect(close_dialog)
	input_field.text_submitted.connect(func(_t): _on_send())

func open_for(npc_id: String, display_name: String) -> void:
	_npc_id = npc_id
	title_label.text = "%s (%s)" % [display_name, npc_id]
	log_label.clear()
	log_label.append_text("[i]Approche un PNJ et parle. Serveur: %s[/i]\n" % Config.AI_SERVER_URL)
	visible = true
	input_field.grab_focus()

func close_dialog() -> void:
	visible = false
	_npc_id = ""

func _on_send() -> void:
	var msg := input_field.text.strip_edges()
	if msg.is_empty() or _npc_id.is_empty():
		return
	log_label.append_text("\n[b]Vous:[/b] %s\n" % msg)
	input_field.text = ""
	send_button.disabled = true
	var url := "%s/npc/%s/talk" % [Config.AI_SERVER_URL, _npc_id]
	var body := JSON.stringify({"message": msg})
	var headers := PackedStringArray(["Content-Type: application/json"])
	var err := _http.request(url, headers, HTTPClient.METHOD_POST, body)
	if err != OK:
		log_label.append_text("[color=red]Erreur HTTPRequest: %s[/color]\n" % err)
		send_button.disabled = false

func _on_request_completed(result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
	send_button.disabled = false
	if result != HTTPRequest.RESULT_SUCCESS:
		log_label.append_text("[color=red]Échec réseau (ai-server démarré ?).[/color]\n")
		return
	if response_code != 200:
		log_label.append_text("[color=red]HTTP %s[/color]\n" % response_code)
		return
	var data = JSON.parse_string(body.get_string_from_utf8())
	if typeof(data) != TYPE_DICTIONARY:
		log_label.append_text("[color=red]Réponse JSON invalide[/color]\n")
		return
	log_label.append_text("[b]%s:[/b] %s\n" % [data.get("npc_name", "PNJ"), data.get("reply", "")])
