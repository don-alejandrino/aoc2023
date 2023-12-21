from __future__ import annotations

import math
import time
from operator import add
from typing import List, Dict, Tuple, Union, Any

EXAMPLE1 = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

EXAMPLE2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


class ModuleRegistry:
    def __init__(self):
        self._registry: dict[str, BroadCaster] = {}
        self._targets: dict[str, List[str]] = {}

    def add(self, module_id, module_type, targets):
        self._targets[module_id] = targets
        if module_type == "%":
            self._registry[module_id] = FlipFlop(module_id)
        elif module_type == "&":
            self._registry[module_id] = Conjunction(module_id)
        elif module_type == "broadcaster":
            self._registry[module_id] = BroadCaster(module_id)
        else:
            raise ValueError("Unknown module type.")

    def reset(self):
        for key, val in self._registry.items():
            self._registry[key] = type(val)(val.id)
        self.register_listeners()

    def register_listeners(self):
        for module_id, target_ids in self._targets.items():
            for target_id in target_ids:
                target_module = self._registry.get(target_id)
                if target_module is not None:
                    if isinstance(target_module, Conjunction):
                        target_module.set_input(module_id)
                else:
                    # Unconnected dead-end modules are not created in the first place
                    target_module = DeadEnd(target_id)
                    self._registry[target_id] = target_module
                self._registry[module_id].register_listeners(target_module)

    def _send_signals(self, from_id: str, check_for_high_pulse_sent_from_module: str) -> Tuple[List[int], bool]:
        sender_queue = [from_id]
        overall_send_stats = [1, 0]
        module_sent_high_pulse = False
        while sender_queue:
            from_id = sender_queue.pop(0)
            sender_module = self._registry[from_id]
            if from_id == check_for_high_pulse_sent_from_module and sender_module.pulse_type == 1:
                module_sent_high_pulse = True
            send_stats, triggered_listeners = sender_module.emit()
            # noinspection PyTypeChecker
            overall_send_stats = list(map(add, overall_send_stats, send_stats))
            for tgt_id in triggered_listeners:
                if tgt_id in self._registry.keys():
                    sender_queue.append(tgt_id)

        return overall_send_stats, module_sent_high_pulse

    def push_button_and_count_signals(
            self, check_for_high_pulse_sent_from_module: str = None
    ) -> Tuple[List[int], bool, int]:
        cycle_stats = self._send_signals("broadcaster", check_for_high_pulse_sent_from_module)

        return cycle_stats[0], cycle_stats[1], create_hash(self.get_module_states())

    def get_module_states(self) -> Dict[str, Union[Dict[str, int], bool]]:
        module_states = {}
        for key, val in self._registry.items():
            if key != "broadcaster":
                module_states[key] = val.get_state()

        return module_states

    def get_parent_modules(self, module_id: str) -> List[str]:
        parent_ids = []
        for key, val in self._targets.items():
            if module_id in val:
                parent_ids.append(key)

        return parent_ids


class BroadCaster:
    def __init__(self, module_id: str):
        self.id: str = module_id
        self._listeners: List[BroadCaster] = []
        # 0: low signal, 1: high signal
        self.pulse_type: int = 0

    def receive(self, from_id: str, pulse_type: int):
        raise NotImplementedError

    def emit(self) -> Tuple[List[int], List[str]]:
        send_stats = [0, 0]
        triggered_listeners = []
        for listener in self._listeners:
            if listener.receive(self.id, self.pulse_type):
                triggered_listeners.append(listener.id)
        send_stats[self.pulse_type] = len(self._listeners)

        return send_stats, triggered_listeners

    def register_listeners(self, listener: BroadCaster):
        self._listeners.append(listener)

    def get_state(self) -> Union[Dict[str, int], bool]:
        raise NotImplementedError


class FlipFlop(BroadCaster):
    def __init__(self, module_id: str):
        super().__init__(module_id)
        self.active: bool = False

    def receive(self, from_id: str, pulse_type: int) -> bool:
        if pulse_type == 0:
            self.active = not self.active
            self.pulse_type = int(self.active)
            triggered = True
        else:
            triggered = False

        return triggered

    def get_state(self) -> bool:
        return self.active


class Conjunction(BroadCaster):
    def __init__(self, module_id: str):
        super().__init__(module_id)
        self._inputs: Dict[str, int] = {}

    def receive(self, from_id: str, pulse_type: int):
        self._inputs[from_id] = pulse_type
        if set(self._inputs.values()) == {1}:
            self.pulse_type = 0
        else:
            self.pulse_type = 1

        return True

    def set_input(self, input_id: str):
        self._inputs[input_id] = 0

    def get_state(self) -> Dict[str, int]:
        return self._inputs


class DeadEnd(BroadCaster):
    def __init__(self, module_id: str):
        super().__init__(module_id)

    def receive(self, from_id: str, pulse_type: int):
        pass

    def get_state(self) -> bool:
        return True


def parse_input(text: str) -> ModuleRegistry:
    mod_reg = ModuleRegistry()
    for line in text.strip().split("\n"):
        src_block, tgt_block = line.strip().split(" -> ")
        src_block = src_block.strip()
        tgt_ids = tgt_block.strip().split(", ")
        if src_block == "broadcaster":
            mod_reg.add("broadcaster", "broadcaster", tgt_ids)
        else:
            mod_reg.add(src_block[1:], src_block[0], tgt_ids)

    return mod_reg


def freeze(obj: Any) -> Any:
    if isinstance(obj, dict):
        return frozenset({k: freeze(v) for k, v in obj.items()}.items())
    elif isinstance(obj, list):
        return tuple([freeze(v) for v in obj])

    return obj


def create_hash(obj: Any) -> int:
    return hash(freeze(obj))


def get_pulse_product(mod_reg: ModuleRegistry, max_num_cycles: int) -> int:
    mod_reg.register_listeners()
    state_hashes = []
    num_signals_in_outer_cycle = [0, 0]
    outer_cycle_periodicity = max_num_cycles
    for i in range(max_num_cycles):
        num_signals, _, state_hash = mod_reg.push_button_and_count_signals()
        if state_hash not in state_hashes:
            state_hashes.append(state_hash)
            # noinspection PyTypeChecker
            num_signals_in_outer_cycle = list(map(add, num_signals_in_outer_cycle, num_signals))
        else:
            outer_cycle_periodicity = i
            break

    num_outer_cycles = max_num_cycles // outer_cycle_periodicity

    return num_signals_in_outer_cycle[0] * num_signals_in_outer_cycle[1] * num_outer_cycles ** 2


def get_num_button_pushes_to_send_low_signal_to_rx(mod_reg: ModuleRegistry) -> int:
    # After analyzing the input (assuming this to be valid for all puzzle inputs, otherwise solving the puzzle could
    # become very hard), we find that rx is connected to a single conjunction module. That is, in order for this
    # conjunction module to emit a low signal, all of its inputs must send a high signal at the same time. Therefore, we
    # calculate the periodicity of all these input modules sending a high signal and get the least common multiple of
    # them. Note that this simple procedure works only because the puzzle input was tailored for that.
    mod_reg.register_listeners()
    rx_parent = mod_reg.get_parent_modules("rx")[0]
    rx_parent_parents = mod_reg.get_parent_modules(rx_parent)

    parent_cycles = []
    for pp in rx_parent_parents:
        pp_module_sent_high_pulse = False
        mod_reg.reset()
        num_pushes = 0
        while not pp_module_sent_high_pulse:
            pp_module_sent_high_pulse = mod_reg.push_button_and_count_signals(pp)[1]
            num_pushes += 1
        parent_cycles.append(num_pushes)

    return math.lcm(*parent_cycles)


if __name__ == "__main__":
    with open("../inputs/input20.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    module_registry = parse_input(in_text)
    res = get_pulse_product(module_registry, 1000)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    module_registry = parse_input(in_text)
    res = get_num_button_pushes_to_send_low_signal_to_rx(module_registry)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
