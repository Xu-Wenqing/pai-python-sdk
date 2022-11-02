from typing import Any, Dict

from pai.api.base import PaginatedResult, ScopeResourceAPI
from pai.libs.alibabacloud_paistudio20220112.client import Client
from pai.libs.alibabacloud_paistudio20220112.models import (
    CreateTrainingJobRequest,
    CreateTrainingJobRequestComputeResource,
    CreateTrainingJobRequestHyperParameters,
    CreateTrainingJobRequestInputChannels,
    CreateTrainingJobRequestLabels,
    CreateTrainingJobRequestOutputChannels,
    CreateTrainingJobRequestScheduler,
    CreateTrainingJobResponseBody,
    GetAlgorithmVersionResponseBody,
    GetTrainingJobResponseBody,
    ListAlgorithmsRequest,
    ListAlgorithmVersionsRequest,
)


class TrainingJobAPI(ScopeResourceAPI):
    _create_method = "create_training_job_with_options"
    _get_method = "get_training_job_with_options"

    # _list_method = "list_training_jobs_with_options"

    def __init__(self, workspace_id: str, acs_client: Client):
        super(TrainingJobAPI, self).__init__(
            workspace_id=workspace_id, acs_client=acs_client
        )

    def list(self, page_size=20, page_number=1):
        pass

    def get_api_object_by_resource_id(self, resource_id) -> Dict[str, Any]:
        res: GetTrainingJobResponseBody = self._do_request(
            method_=self._get_method,
            training_job_id=resource_id,
        )
        return res.to_map()

    def get(self, training_job_id) -> Dict[str, Any]:
        return self.get_api_object_by_resource_id(training_job_id)

    def create(
        self,
        instance_type,
        instance_count,
        job_name,
        hyperparameters: Dict[str, Any] = None,
        input_channels=None,
        output_channels=None,
        labels=None,
        max_running_in_seconds=None,
        description=None,
        algorithm_name=None,
        algorithm_version=None,
        algorithm_provider=None,
    ) -> str:
        input_channels = [
            CreateTrainingJobRequestInputChannels().from_map(ch)
            for ch in input_channels
        ]
        output_channels = [
            CreateTrainingJobRequestOutputChannels().from_map(ch)
            for ch in output_channels
        ]

        request = CreateTrainingJobRequest(
            algorithm_name=algorithm_name,
            algorithm_provider=algorithm_provider,
            algorithm_version=algorithm_version,
            compute_resource=CreateTrainingJobRequestComputeResource(
                ecs_count=instance_count,
                ecs_spec=instance_type,
            ),
            hyper_parameters=[
                CreateTrainingJobRequestHyperParameters(
                    name=name,
                    value=str(value),
                )
                for name, value in hyperparameters.items()
            ],
            input_channels=input_channels,
            labels=[
                CreateTrainingJobRequestLabels(key=key, value=value)
                for key, value in labels.items()
            ]
            if labels
            else None,
            output_channels=output_channels,
            scheduler=CreateTrainingJobRequestScheduler(
                max_running_time_in_seconds=max_running_in_seconds
            ),
            training_job_description=description,
            training_job_name=job_name,
            workspace_id=self.workspace_id,
        )

        resp: CreateTrainingJobResponseBody = self._do_request(
            method_=self._create_method, request=request
        )

        return resp.training_job_id