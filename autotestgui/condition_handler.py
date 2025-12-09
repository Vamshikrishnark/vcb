"""
Conditional Execution Handler for Test Steps

This module handles all conditional logic for determining whether a test step
should execute based on various conditions and previous step results.
"""

class ConditionHandler:
    """Handles evaluation of step execution conditions"""
    
    # Available condition types
    CONDITIONS = [
        "Always",
        "If Previous Passed",
        "If Previous Failed",
        "If Previous Skipped",
        "If All Previous Passed",
        "If Any Previous Failed",
        "If Specific Step Passed",
        "If Specific Step Failed",
        "On Error Only",
        "On Success Only",
        "Skip"
    ]
    
    def __init__(self):
        self.step_history = []  # Track all step results
    
    def reset_history(self):
        """Reset step history for a new test case execution"""
        self.step_history = []
    
    def record_step_result(self, step_index, step_name, result, was_skipped=False):
        """
        Record a step's execution result
        
        Args:
            step_index: The step number (1-based)
            step_name: Name of the step
            result: 'PASS', 'FAIL', 'ERROR', or None
            was_skipped: Whether the step was skipped
        """
        self.step_history.append({
            'index': step_index,
            'name': step_name,
            'result': result,
            'skipped': was_skipped
        })
    
    def should_run_step(self, step_index, condition, total_steps=None, target_step=None):
        """
        Determine if a step should run based on its condition
        
        Args:
            step_index: Current step number (1-based)
            condition: The run condition string
            total_steps: Total number of steps (optional)
            target_step: Target step number for specific step conditions (optional)
        
        Returns:
            tuple: (should_run: bool, skip_reason: str or None)
        """
        # Always run if condition is "Always"
        if condition == "Always":
            return True, None
        
        # Always skip if condition is "Skip"
        if condition == "Skip":
            return False, "Marked as Skip"
        
        # Get previous step result (if exists)
        previous_step = self.step_history[-1] if self.step_history else None
        
        # Handle conditions based on previous step
        if condition == "If Previous Passed":
            if step_index == 1:
                return False, "No previous step to check"
            if previous_step is None:
                return False, "Previous step had no result"
            if previous_step['skipped']:
                return False, "Previous step was skipped"
            if previous_step['result'] != 'PASS':
                return False, "Previous step failed"
            return True, None
        
        elif condition == "If Previous Failed":
            if step_index == 1:
                return False, "No previous step to check"
            if previous_step is None:
                return False, "Previous step had no result"
            if previous_step['skipped']:
                return False, "Previous step was skipped"
            if previous_step['result'] == 'PASS':
                return False, "Previous step passed"
            return True, None
        
        elif condition == "If Previous Skipped":
            if step_index == 1:
                return False, "No previous step to check"
            if previous_step is None or not previous_step['skipped']:
                return False, "Previous step was not skipped"
            return True, None
        
        # Handle conditions based on all previous steps
        elif condition == "If All Previous Passed":
            if step_index == 1:
                return True, None  # No previous steps, so condition is met
            
            executed_steps = [s for s in self.step_history if not s['skipped']]
            if not executed_steps:
                return False, "No previous steps were executed"
            
            if all(s['result'] == 'PASS' for s in executed_steps):
                return True, None
            else:
                return False, "Not all previous steps passed"
        
        elif condition == "If Any Previous Failed":
            if step_index == 1:
                return False, "No previous steps to check"
            
            executed_steps = [s for s in self.step_history if not s['skipped']]
            if not executed_steps:
                return False, "No previous steps were executed"
            
            if any(s['result'] in ['FAIL', 'ERROR'] for s in executed_steps):
                return True, None
            else:
                return False, "No previous steps failed"
        
        elif condition == "On Error Only":
            if step_index == 1:
                return False, "No previous steps to check"
            
            if any(s['result'] == 'ERROR' for s in self.step_history if not s['skipped']):
                return True, None
            else:
                return False, "No previous errors detected"
        
        elif condition == "On Success Only":
            if step_index == 1:
                return True, None  # First step can run
            
            executed_steps = [s for s in self.step_history if not s['skipped']]
            if not executed_steps:
                return False, "No previous steps were executed"
            
            if all(s['result'] == 'PASS' for s in executed_steps):
                return True, None
            else:
                return False, "Some previous steps failed"
        
        # Handle specific step conditions
        elif condition == "If Specific Step Passed":
            if target_step is None:
                return False, "No target step specified"
            
            if target_step >= step_index:
                return False, f"Target step {target_step} has not executed yet"
            
            # Find the specific step in history
            target_step_data = None
            for s in self.step_history:
                if s['index'] == target_step:
                    target_step_data = s
                    break
            
            if target_step_data is None:
                return False, f"Step {target_step} not found in history"
            
            if target_step_data['skipped']:
                return False, f"Step {target_step} was skipped"
            
            if target_step_data['result'] == 'PASS':
                return True, None
            else:
                return False, f"Step {target_step} did not pass"
        
        elif condition == "If Specific Step Failed":
            if target_step is None:
                return False, "No target step specified"
            
            if target_step >= step_index:
                return False, f"Target step {target_step} has not executed yet"
            
            # Find the specific step in history
            target_step_data = None
            for s in self.step_history:
                if s['index'] == target_step:
                    target_step_data = s
                    break
            
            if target_step_data is None:
                return False, f"Step {target_step} not found in history"
            
            if target_step_data['skipped']:
                return False, f"Step {target_step} was skipped"
            
            if target_step_data['result'] in ['FAIL', 'ERROR']:
                return True, None
            else:
                return False, f"Step {target_step} did not fail"
        
        # Default: run the step
        return True, None
    
    def get_execution_summary(self):
        """
        Get a summary of step execution history
        
        Returns:
            dict: Summary statistics
        """
        total = len(self.step_history)
        executed = len([s for s in self.step_history if not s['skipped']])
        skipped = len([s for s in self.step_history if s['skipped']])
        passed = len([s for s in self.step_history if s['result'] == 'PASS' and not s['skipped']])
        failed = len([s for s in self.step_history if s['result'] in ['FAIL', 'ERROR'] and not s['skipped']])
        
        return {
            'total': total,
            'executed': executed,
            'skipped': skipped,
            'passed': passed,
            'failed': failed
        }
