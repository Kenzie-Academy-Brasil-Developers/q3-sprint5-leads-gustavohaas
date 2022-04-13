from flask import Blueprint
from app.controllers import lead_controller

bp = Blueprint("leads", __name__, url_prefix="/leads")

bp.post("")(lead_controller.create_lead)
bp.get("")(lead_controller.get_leads)
bp.patch("")(lead_controller.update_lead)
bp.delete("")(lead_controller.delete_lead)
