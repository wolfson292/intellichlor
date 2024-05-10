import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID
from esphome import automation
from esphome.automation import maybe_simple_id
from esphome.cpp_helpers import gpio_pin_expression
from esphome.const import (
    CONF_FLOW_CONTROL_PIN,
)
from esphome import pins

DEPENDENCIES = ["uart"]
CODEOWNERS = ["@wolfson292"]
MULTI_CONF = True

intellichlor_ns = cg.esphome_ns.namespace("intellichlor")
INTELLICHLORComponent = intellichlor_ns.class_("INTELLICHLORComponent", cg.PollingComponent, uart.UARTDevice)

CONF_INTELLICHLOR_ID = "intellichlor_id"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(INTELLICHLORComponent),
        cv.Optional(CONF_FLOW_CONTROL_PIN): pins.gpio_output_pin_schema,
    }
)

CONFIG_SCHEMA = cv.All(
    CONFIG_SCHEMA.extend(uart.UART_DEVICE_SCHEMA).extend(cv.polling_component_schema('60s'))
)

FINAL_VALIDATE_SCHEMA = uart.final_validate_device_schema(
    "intellichlor",
    require_tx=True,
    require_rx=True,
    parity="NONE",
    stop_bits=1,
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_FLOW_CONTROL_PIN in config:
        pin = await gpio_pin_expression(config[CONF_FLOW_CONTROL_PIN])
        cg.add(var.set_flow_control_pin(pin))

CALIBRATION_ACTION_SCHEMA = maybe_simple_id(
    {
        cv.Required(CONF_ID): cv.use_id(INTELLICHLORComponent),
    }
)
