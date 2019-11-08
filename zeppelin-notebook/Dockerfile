#
# Copyright (c) 2019 Intel Corporation
#
# Main author:
#   * otc-swstacks <otc-swstacks@intel.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
FROM clearlinux/stacks-dars-mkl:v0.1.2
LABEL maintainer=otc-swstacks@intel.com

COPY requirements.txt /
RUN pip install -r requirements.txt

ENV SPARK_MASTER_PORT=7077
ENV ZEPPELIN_HOME /opt/zeppelin

EXPOSE 4040 7077 8080 8081 8082

COPY scripts/entrypoint.sh /opt/
ENTRYPOINT ["/opt/entrypoint.sh"]
CMD []