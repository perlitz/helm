from typing import Optional

from helm.benchmark.model_deployment_registry import (
    ClientSpec,
    ModelDeployment,
    WindowServiceSpec,
    register_model_deployment,
)
from helm.benchmark.tokenizer_config_registry import TokenizerConfig, TokenizerSpec, register_tokenizer_config


def register_huggingface_model(
    helm_model_name: str, pretrained_model_name_or_path: str, revision: Optional[str] = None
) -> None:
    object_spec_args = {"pretrained_model_name_or_path": pretrained_model_name_or_path}
    if revision:
        object_spec_args["revision"] = revision

    model_deployment = ModelDeployment(
        name=helm_model_name,
        client_spec=ClientSpec(
            class_name="helm.proxy.clients.huggingface_client.HuggingFaceClient",
            args=object_spec_args,
        ),
        model_name=helm_model_name,
        tokenizer_name=helm_model_name,
        window_service_spec=WindowServiceSpec(
            class_name="helm.benchmark.window_services.huggingface_window_service.HuggingFaceWindowService",
            args=object_spec_args,
        ),
    )
    register_model_deployment(model_deployment)
    tokenizer_config = TokenizerConfig(
        name=helm_model_name,
        tokenizer_spec=TokenizerSpec(
            class_name="helm.proxy.clients.huggingface_client.HuggingFaceClient",
            args=object_spec_args,
        ),
    )
    register_tokenizer_config(tokenizer_config)


def register_huggingface_hub_model_from_flag_value(flag_value: str) -> None:
    raw_model_string_parts = flag_value.split("@")
    pretrained_model_name_or_path: str
    revision: Optional[str]
    if len(raw_model_string_parts) == 1:
        pretrained_model_name_or_path, revision = raw_model_string_parts[0], None
    elif len(raw_model_string_parts) == 2:
        pretrained_model_name_or_path, revision = raw_model_string_parts
    else:
        raise ValueError(
            f"Could not parse Hugging Face flag value: '{flag_value}'; "
            "Expected format: namespace/model_engine[@revision]"
        )
    register_huggingface_model(
        helm_model_name=flag_value,
        pretrained_model_name_or_path=pretrained_model_name_or_path,
        revision=revision,
    )


def register_huggingface_local_model_from_flag_value(flag_value: str) -> None:
    raw_model_string_parts = flag_value.split("@")
    pretrained_model_name_or_path: str
    revision: Optional[str]
    if len(raw_model_string_parts) == 1:
        pretrained_model_name_or_path, revision = raw_model_string_parts[0], None
    elif len(raw_model_string_parts) == 2:
        pretrained_model_name_or_path, revision = raw_model_string_parts
    register_huggingface_model(
        helm_model_name=flag_value,
        pretrained_model_name_or_path=pretrained_model_name_or_path,
        revision=revision,
    )
