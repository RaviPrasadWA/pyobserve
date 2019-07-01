import sys


class context():
    """ Debug context to trace any function calls inside the context """

    def __init__(self, name, mappings, func):
        self.variables_mappings = mappings
        self.name = name
        self.history_ = {}
        self.func = func

    def __enter__(self):
        # Set the trace function to the trace_calls function
        # So all events are now traced
        sys.settrace(self.trace_calls)

    def __exit__(self, *args, **kwargs):
        # Stop tracing all events
        sys.settrace = None

    def trace_calls(self, frame, event, arg):
        # We want to only trace our call to the decorated function
        if event != 'call':
            return
        elif frame.f_code.co_name != self.name:
            return
        # return the trace function to use when you go into that
        # function call
        return self.trace_lines

    def debug_function(self, **kwargs):
        print(kwargs)

    def perform_action(self, variable, var_value, definition, local_vars, message, frame, debug=True):
        var_history = self.history_.get(variable, None)

        def perform(type_, variable, var_value, definition, exec_func=True):
            if exec_func:
                lock_execution = False
                function_ = definition.get(type_, None)

                if type_ == "on-range":
                    sequences = function_.get("sequences")
                    operation = function_.get("operation", None)
                    function_ = function_.get("function", None)

                    final_sequences = []
                    for sequence in sequences:
                        if "->" in sequence:
                            _ = sequence.split("->")
                            analogy, var_ = _[0], _[1]
                            if analogy == "var":
                                val = local_vars.get(var_, None)
                                if val:
                                    final_sequences.append(val)
                    print(final_sequences)



                if type_ == "on-specific":
                    target_value = function_.get("target_value")
                    update_value = function_.get("update_value", None)
                    function_ = function_.get("function", None)
                    if target_value != var_value:
                        lock_execution = True
                    else:
                        if update_value:
                            frame.f_locals.update({variable: update_value})

                if function_:
                    if lock_execution is False:
                        return_ = function_(variable=variable,
                                            value=var_value,
                                            type_=type_)
                        if return_:
                            if "inject" in return_.keys():
                                try:
                                    func_globals = self.func.__globals__  # Python 2.6+
                                except AttributeError:
                                    func_globals = self.func.func_globals  # Earlier versions.

                                saved_values = func_globals.copy()  # Shallow copy of dict.
                                func_globals.update(return_["inject"])

                            if "update" in return_.keys():
                                frame.f_locals.update(return_["update"])

            self.history_[variable] = var_value

        if var_history is None:
            if variable in local_vars:
                if "on-create" in definition.keys():
                    perform("on-create", variable, var_value, definition)
                else:
                    perform("on-create", variable, var_value, definition, exec_func=False)

        if var_history is not None:
            if variable in local_vars:
                if var_value != var_history:
                    if "on-change" in definition.keys():
                        perform("on-change", variable, var_value, definition)

                if "on-specific" in definition.keys():
                    perform("on-specific", variable, var_value, definition)

                if "on-range" in definition.keys():
                    perform("on-range", variable, var_value, definition)

            if "on-delete" in definition.keys():
                if var_value is None:
                    perform("on-delete", variable, var_value, definition)

        if debug:
            self.debug_function(message=message)

    def trace_lines(self, frame, event, arg):
        # If you want to print local variables each line
        # keep the check for the event 'line'
        # If you want to print local variables only on return
        # check only for the 'return' event
        if event not in ['line', 'return']:
            return
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename
        local_vars = frame.f_locals
        message = ('{0} {1} {2} locals: {3}'.format(func_name,
                                                    event,
                                                    line_no,
                                                    local_vars))

        for variable in self.variables_mappings.keys():
            definition = self.variables_mappings[variable]
            var_value = local_vars.get(variable, None)
            self.perform_action(variable, var_value, definition, local_vars, message, frame, debug=False)


def observer(mappings):
    def detector(func, *args, **kwargs):
        """ Debug decorator to call the function within the debug context """

        def wrapper(*args, **kwargs):
            with context(func.__name__, mappings, func):
                return_value = func(*args, **kwargs)
            return return_value

        return wrapper

    return detector
